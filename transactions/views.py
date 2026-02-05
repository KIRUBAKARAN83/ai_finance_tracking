# transactions/views.py
# ===============================
# Standard library
# ===============================
import json
from datetime import date, timedelta

# ===============================
# Django core
# ===============================
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
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

# Optional models (may not exist yet after DB reset)
try:
    from accounts.models import UserActivity
except Exception:
    UserActivity = None

# ===============================
# Insights / AI services (OPTIONAL)
# ===============================
try:
    from insights.services import monthly_summary
    from insights.health_score import financial_health_score
    from insights.budget_alerts import budget_alerts
    from insights.month_compare import month_comparison
    from insights.budget_progress import budget_progress
    from insights.budget_suggest import suggest_budgets
    from insights.chat_engine import finance_chat, finance_chat_stream
except Exception as e:
    print("INSIGHTS IMPORT ERROR:", e)
    monthly_summary = budget_alerts = financial_health_score = None
    month_comparison = budget_progress = suggest_budgets = None
    finance_chat = finance_chat_stream = None

app_name="transactions"


# =========================================================
# DASHBOARD (HARDENED)
# =========================================================
@login_required
def dashboard(request):
    # Render health check (HEAD /)
    if request.method == "HEAD":
        return HttpResponse(status=200)

    today = date.today()

    # Safe defaults
    summary = {"income": 0, "expense": 0, "savings": 0, "insights": []}
    alerts = []
    health = {}
    comparison = {}
    budgets = []

    try:
        if monthly_summary:
            summary = monthly_summary(request.user, today.month, today.year) or summary
            summary.setdefault("insights", [])

        if budget_alerts:
            alerts = budget_alerts(request.user) or []
            summary["insights"].extend(alerts)

        if financial_health_score:
            health = financial_health_score(request.user) or {}

        if month_comparison:
            comparison = month_comparison(request.user) or {}

        if budget_progress:
            budgets = budget_progress(request.user) or []

    except Exception as e:
        print("DASHBOARD ERROR:", e)

    # Transactions list
    qs = Transaction.objects.filter(
        user=request.user,
        date__month=today.month,
        date__year=today.year,
    )

    query = request.GET.get("q", "").strip()
    if query:
        qs = qs.filter(
            Q(category__icontains=query)
            | Q(note__icontains=query)
            | Q(transaction_type__icontains=query)
        )

    transactions = Paginator(qs.order_by("-date"), 10).get_page(
        request.GET.get("page")
    )

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
        return redirect("transactions:dashboard")
    return render(request, "transaction_form.html", {"form": form})


@login_required
def edit_transaction(request, pk):
    txn = get_object_or_404(Transaction, pk=pk, user=request.user)
    form = TransactionForm(request.POST or None, instance=txn)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("transactions:dashboard")
    return render(request, "transaction_form.html", {"form": form})


@login_required
def delete_transaction(request, pk):
    txn = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == "POST":
        txn.delete()
        return redirect("transactions:dashboard")
    return render(request, "confirm_delete.html", {"transaction": txn})


# =========================================================
# CHART DATA
# =========================================================
@login_required
def chart_data(request):
    today = date.today()

    income = (
        Transaction.objects.filter(
            user=request.user,
            transaction_type="INCOME",
            date__month=today.month,
            date__year=today.year,
        ).aggregate(total=Sum("amount"))["total"]
        or 0
    )

    expense = (
        Transaction.objects.filter(
            user=request.user,
            transaction_type="EXPENSE",
            date__month=today.month,
            date__year=today.year,
        ).aggregate(total=Sum("amount"))["total"]
        or 0
    )

    return JsonResponse(
        {
            "income": float(income),
            "expense": float(expense),
            "savings": float(income - expense),
        }
    )


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

    start = request.GET.get("start")
    end = request.GET.get("end")
    if start:
        qs = qs.filter(date__gte=start)
    if end:
        qs = qs.filter(date__lte=end)

    transactions = Paginator(qs.order_by("-date"), 15).get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "all_transaction.html",
        {
            "transactions": transactions,
            "query": query,
            "start_date": start,
            "end_date": end,
        },
    )


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
        return redirect("transactions:dashboard")

    try:
        suggestions = suggest_budgets(request.user) if suggest_budgets else []
    except Exception as e:
        print("BUDGET SUGGEST ERROR:", e)
        suggestions = []

    return render(
        request,
        "budget_form.html",
        {"form": form, "suggestions": suggestions},
    )


@login_required
def budgets_list(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request, "budgets_list.html", {"budgets": budgets})

@login_required
def delete_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    budget.delete()
    return redirect("transactions:budgets_list")  # redirect back to list after deletion


# =========================================================
# AI CHAT (NEVER 500)
# =========================================================
@login_required
@require_POST
def chat_api(request):
    try:
        data = json.loads(request.body or "{}")
        msg = (data.get("message") or "").strip()

        if not msg:
            return JsonResponse({"reply": "Ask something 🙂"})

        if not finance_chat:
            return JsonResponse({"reply": "AI is disabled."})

        reply = finance_chat(request.user, msg)
        return JsonResponse({"reply": reply or "⚠️ No response."})

    except Exception as e:
        print("CHAT ERROR:", e)
        return JsonResponse(
            {"reply": "⚠️ AI temporarily unavailable."},
            status=200,
        )


@login_required
@require_POST
def chat_stream(request):
    if not finance_chat_stream:
        return StreamingHttpResponse("AI disabled.", content_type="text/plain")

    try:
        data = json.loads(request.body or "{}")
        message = (data.get("message") or "").strip()
    except Exception:
        message = ""

    def event_stream():
        try:
            for token in finance_chat_stream(request.user, message):
                yield token
        except Exception as e:
            print("CHAT STREAM ERROR:", e)
            yield "\n⚠️ AI error"

    return StreamingHttpResponse(event_stream(), content_type="text/plain")


# =========================================================
# ADMIN
# =========================================================
@staff_member_required
def admin_dashboard(request):
    try:
        online_users = (
            UserActivity.objects.filter(
                last_seen__gte=now() - timedelta(minutes=5)
            ).count()
            if UserActivity
            else 0
        )
    except Exception:
        online_users = 0

    total_income = (
        Transaction.objects.filter(transaction_type="INCOME")
        .aggregate(total=Sum("amount"))["total"]
        or 0
    )

    total_expense = (
        Transaction.objects.filter(transaction_type="EXPENSE")
        .aggregate(total=Sum("amount"))["total"]
        or 0
    )

    return render(
        request,
        "admin_dashboard.html",
        {
            "total_users": User.objects.count(),
            "online_users": online_users,
            "total_income": total_income,
            "total_expense": total_expense,
            "total_transactions": Transaction.objects.count(),
        },
    )


@staff_member_required
def admin_users(request):
    return render(
        request,
        "admin_users.html",
        {"users": User.objects.all().order_by("-date_joined")},
    )


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

import matplotlib
matplotlib.use("Agg")  # REQUIRED for servers (no GUI)

import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.contrib.auth.decorators import login_require
from datetime import date

from insights.services import category_breakdown


@login_required
def expense_category_chart(request):
    """
    Generates a bar chart of expenses by category for the current month
    and returns it as a PNG image response.
    """

    today = date.today()

    # Get expense breakdown for the logged-in user
    df = category_breakdown(request.user, today.month, today.year)

    if df.empty:
        return HttpResponse("No data available", status=204)

    # Create the chart
    plt.figure(figsize=(6, 4))
    plt.bar(df["category"], df["total"], color="#6F4FF2")
    plt.title("Expense by Category (₹)")
    plt.xlabel("Category")
    plt.ylabel("Amount (₹)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    # Return chart as PNG
    response = HttpResponse(content_type="image/png")
    plt.savefig(response, format="png", dpi=120)
    plt.close()

    return response
    #return render(request, "expense_category_chart.html")

"""from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#@login_required
def expense_category_page(request):
    
    Renders the page that shows the chart and provides export option.
    
    return render(request, "expense_category_page.html")"""


