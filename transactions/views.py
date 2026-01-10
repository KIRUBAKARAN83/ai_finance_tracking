# ===============================
# Standard library
# ===============================
import json
from datetime import date, timedelta

# ===============================
# Django core
# ===============================
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum, Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.utils.timezone import now

# ===============================
# Local app imports
# ===============================
from .models import Transaction, Budget
from .forms import TransactionForm, BudgetForm
from accounts.models import UserActivity

# ===============================
# Insights / AI services
# ===============================
from insights.services import monthly_summary
from insights.health_score import financial_health_score
from insights.budget_alerts import budget_alerts
from insights.month_compare import month_comparison
from insights.budget_progress import budget_progress
from insights.budget_suggest import suggest_budgets
from insights.chat_engine import finance_chat


# =========================================================
# USER DASHBOARD
app_name="transactions"
# =========================================================
@login_required(login_url="login")
def dashboard(request):
    today = date.today()

    # ---- SAFE DEFAULTS ----
    summary = {"income": 0, "expense": 0, "savings": 0, "insights": []}
    alerts = []
    health = {}
    comparison = {}
    budgets = []

    try:
        summary = monthly_summary(request.user, today.month, today.year) or summary
        summary.setdefault("insights", [])

        alerts = budget_alerts(request.user) or []
        health = financial_health_score(request.user) or {}
        comparison = month_comparison(request.user) or {}
        budgets = budget_progress(request.user) or []

        summary["insights"].extend(alerts)

    except Exception as e:
        print("DASHBOARD ERROR:", e)

    # ---- TRANSACTIONS ----
    query = request.GET.get("q", "").strip()
    transactions_qs = Transaction.objects.filter(
        user=request.user,
        date__month=today.month,
        date__year=today.year,
    )

    if query:
        transactions_qs = transactions_qs.filter(
            Q(category__icontains=query)
            | Q(note__icontains=query)
            | Q(transaction_type__icontains=query)
        )

    transactions = Paginator(
        transactions_qs.order_by("-date"), 10
    ).get_page(request.GET.get("page"))

    return render(
        request,
        "dashboard.html",
        {
            **summary,
            **health,
            "alerts": alerts,
            "comparison": comparison,
            "budgets": budgets,
            "transactions": transactions,
            "query": query,
        },
    )


# =========================================================
# TRANSACTION CRUD
# =========================================================
@login_required
def add_transaction(request):
    form = TransactionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        txn = form.save(commit=False)
        txn.user = request.user
        txn.save()
        return redirect("dashboard")
    return render(request, "transaction_form.html", {"form": form})


@login_required
def edit_transaction(request, pk):
    txn = get_object_or_404(Transaction, pk=pk, user=request.user)
    form = TransactionForm(request.POST or None, instance=txn)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("dashboard")
    return render(request, "transaction_form.html", {"form": form})


@login_required
def delete_transaction(request, pk):
    txn = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == "POST":
        txn.delete()
        return redirect("dashboard")
    return render(request, "confirm_delete.html", {"transaction": txn})


# =========================================================
# CHART DATA (AJAX)
# =========================================================
@login_required
def chart_data(request):
    today = date.today()

    income = Transaction.objects.filter(
        user=request.user,
        transaction_type="INCOME",
        date__month=today.month,
        date__year=today.year,
    ).aggregate(total=Sum("amount"))["total"] or 0

    expense = Transaction.objects.filter(
        user=request.user,
        transaction_type="EXPENSE",
        date__month=today.month,
        date__year=today.year,
    ).aggregate(total=Sum("amount"))["total"] or 0

    return JsonResponse({
        "income": float(income),
        "expense": float(expense),
        "savings": float(income - expense),
    })


# =========================================================
# ALL TRANSACTIONS
# =========================================================
@login_required
def all_transactions(request):
    qs = Transaction.objects.filter(user=request.user)

    query = request.GET.get("q", "").strip()
    if query:
        qs = qs.filter(
            Q(category__icontains=query)
            | Q(note__icontains=query)
            | Q(transaction_type__icontains=query)
        )

    if request.GET.get("start"):
        qs = qs.filter(date__gte=request.GET["start"])
    if request.GET.get("end"):
        qs = qs.filter(date__lte=request.GET["end"])

    transactions = Paginator(qs.order_by("-date"), 15).get_page(request.GET.get("page"))

    return render(request, "all_transaction.html", {
        "transactions": transactions,
        "query": query,
    })


# =========================================================
# BUDGETS
# =========================================================
@login_required
def create_budget(request):
    form = BudgetForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        budget = form.save(commit=False)
        budget.user = request.user
        budget.save()
        return redirect("dashboard")
    return render(request, "budget_form.html", {
        "form": form,
        "suggestions": suggest_budgets(request.user),
    })


@login_required
def budgets_list(request):
    return render(request, "budgets_list.html", {
        "budgets": Budget.objects.filter(user=request.user)
    })


# =========================================================
# AI CHATBOT API (HARDENED)
# =========================================================
@login_required
@require_POST
def chat_api(request):
    try:
        data = json.loads(request.body or "{}")
        msg = (data.get("message") or "").strip()

        if not msg:
            return JsonResponse({"reply": "Ask something 🙂"})

        reply = finance_chat(request.user, msg)
        if not reply:
            reply = "⚠️ AI did not return a response."

        return JsonResponse({"reply": str(reply)})

    except Exception as e:
        print("CHAT ERROR:", e)
        return JsonResponse(
            {"reply": "⚠️ AI service temporarily unavailable."},
            status=200,  # IMPORTANT: no 500 to frontend
        )


# =========================================================
# ADMIN (SAFE)
# =========================================================
@staff_member_required
def admin_dashboard(request):
    try:
        online_users = UserActivity.objects.filter(
            last_seen__gte=now() - timedelta(minutes=5)
        ).count()
    except Exception:
        online_users = 0

    return render(request, "admin_dashboard.html", {
        "total_users": User.objects.count(),
        "online_users": online_users,
        "total_income": Transaction.objects.filter(
            transaction_type="INCOME"
        ).aggregate(total=Sum("amount"))["total"] or 0,
        "total_expense": Transaction.objects.filter(
            transaction_type="EXPENSE"
        ).aggregate(total=Sum("amount"))["total"] or 0,
        "total_transactions": Transaction.objects.count(),
    })


@staff_member_required
def admin_users(request):
    return render(request, "admin_users.html", {
        "users": User.objects.all().order_by("-date_joined")
    })


@staff_member_required
def ban_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not user.is_superuser:
        user.is_active = False
        user.save()
    return redirect("transactions:admin_users")


@staff_member_required
def unban_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    return redirect("transactions:admin_users")


@staff_member_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST" and not user.is_superuser:
        user.delete()
    return redirect("transactions:admin_users")


# =========================================================
# PWA OFFLINE
# =========================================================
def offline(request):
    return render(request, "offline.html")

@login_required
def chat_stream(request):
    data = json.loads(request.body)
    message = data.get("message", "").strip()

    def event_stream():
        try:
            for token in finance_chat_stream(request.user, message):
                yield token
        except Exception:
            yield "\n⚠️ AI error"

    return StreamingHttpResponse(
        event_stream(),
        content_type="text/plain"
    )
