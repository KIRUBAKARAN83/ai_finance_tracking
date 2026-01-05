from django.db.models import Sum
from transactions.models import Transaction
from datetime import date
import calendar



def monthly_summary(user, month=None, year=None):
    """
    Basic monthly finance summary (₹ INR)
    """

    today = date.today()
    month = month or today.month
    year = year or today.year

    income = Transaction.objects.filter(
        user=user,
        transaction_type="INCOME",
        date__month=month,
        date__year=year
    ).aggregate(total=Sum("amount"))["total"] or 0

    expense = Transaction.objects.filter(
        user=user,
        transaction_type="EXPENSE",
        date__month=month,
        date__year=year
    ).aggregate(total=Sum("amount"))["total"] or 0

    insights = []

    if expense > income:
        insights.append(
            f"Warning: You spent ₹{expense - income} more than your income this month."
        )
    else:
        insights.append(
            f"You saved ₹{income - expense} this month."
        )

    return {
        "income": income,
        "expense": expense,
        "savings": income - expense,
        "insights": insights,
    }


def category_breakdown(user, month=None, year=None):
    """
    Expense breakdown by category
    """

    today = date.today()
    month = month or today.month
    year = year or today.year

    return (
        Transaction.objects.filter(
            user=user,
            transaction_type="EXPENSE",
            date__month=month,
            date__year=year
        )
        .values("category")
        .annotate(total=Sum("amount"))
    )



def advanced_monthly_insights(user):
    today = date.today()

    curr_month = today.month
    curr_year = today.year

    income = Transaction.objects.filter(
        user=user,
        transaction_type="INCOME",
        date__month=curr_month,
        date__year=curr_year
    ).aggregate(total=Sum("amount"))["total"] or 0

    expense = Transaction.objects.filter(
        user=user,
        transaction_type="EXPENSE",
        date__month=curr_month,
        date__year=curr_year
    ).aggregate(total=Sum("amount"))["total"] or 0

    insights = []

    if expense > income:
        insights.append(f"Warning: Overspent ₹{expense - income}")
    else:
        insights.append(f"Saved ₹{income - expense}")

    return {
        "current_income": income,
        "current_expense": expense,
        "savings": income - expense,
        "insights": insights,
        "month_name": calendar.month_name[curr_month],
    }

from datetime import date
from .models import Insight
from .budget_alerts import budget_alerts


def generate_daily_insights(user):
    today = date.today()
    messages = budget_alerts(user)

    for msg in messages:
        Insight.objects.get_or_create(
            user=user,
            date=today,
            defaults={"text": msg},
        )
    return messages





