from django.db.models import Sum
from datetime import date
from transactions.models import Transaction, Budget

def financial_health_score(user):
    today = date.today()

    income = Transaction.objects.filter(
        user=user,
        transaction_type="INCOME",
        date__month=today.month,
        date__year=today.year
    ).aggregate(total=Sum("amount"))["total"] or 0

    expense = Transaction.objects.filter(
        user=user,
        transaction_type="EXPENSE",
        date__month=today.month,
        date__year=today.year
    ).aggregate(total=Sum("amount"))["total"] or 0

    # ---- Savings Rate (40 pts) ----
    savings_rate = 0
    if income > 0:
        savings_rate = max((income - expense) / income, 0)

    savings_score = min(savings_rate * 40, 40)

    # ---- Expense Control (30 pts) ----
    expense_ratio = expense / income if income > 0 else 1
    expense_score = max(30 - (expense_ratio * 30), 0)

    # ---- Budget Discipline (20 pts) ----
    budgets = Budget.objects.filter(user=user)
    violations = 0

    for b in budgets:
        spent = Transaction.objects.filter(
            user=user,
            category=b.category,
            transaction_type="EXPENSE",
            date__month=today.month,
            date__year=today.year
        ).aggregate(total=Sum("amount"))["total"] or 0

        if spent > b.limit:
            violations += 1

    budget_score = max(20 - (violations * 5), 0)

    # ---- Income Stability (10 pts) ----
    income_score = 10 if income > 0 else 0

    total_score = round(
        savings_score + expense_score + budget_score + income_score
    )

    # ---- Grade ----
    if total_score >= 80:
        grade = "Excellent"
        color = "success"
    elif total_score >= 60:
        grade = "Good"
        color = "primary"
    elif total_score >= 40:
        grade = "Average"
        color = "warning"
    else:
        grade = "Poor"
        color = "danger"

    return {
        "health_score": total_score,
        "health_grade": grade,
        "health_color": color,
    }
