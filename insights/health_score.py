from django.db.models import Sum
from transactions.models import Transaction
from datetime import date

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

    score = 0
    insights = []

    if income > 0:
        savings_rate = (income - expense) / income * 100

        if savings_rate >= 30:
            score += 40
            insights.append("Excellent savings rate.")
        elif savings_rate >= 15:
            score += 25
            insights.append("Moderate savings rate.")
        else:
            score += 10
            insights.append("Low savings rate.")

    if expense <= income:
        score += 30
        insights.append("Expenses under control.")
    else:
        insights.append("Overspending detected.")

    score += 30  # Stability base score

    return {
        "health_score": min(score, 100),
        "health_insights": insights
    }
