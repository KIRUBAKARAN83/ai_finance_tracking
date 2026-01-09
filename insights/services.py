# insights/services.py
from datetime import date
import calendar
from django.db.models import Sum

# Import Insight and budget_alerts at module level (these are local to insights)
from .models import Insight
from .budget_alerts import budget_alerts


def _safe_aggregate(queryset, field="amount"):
    """
    Helper: return aggregated sum or 0 if None or on error.
    """
    try:
        total = queryset.aggregate(total=Sum(field))["total"]
        return total or 0
    except Exception as e:
        print("AGGREGATE ERROR:", e)
        return 0


def monthly_summary(user, month=None, year=None):
    """
    Basic monthly finance summary (₹ INR)
    Returns a dict with income, expense, savings and insights.
    """
    today = date.today()
    month = month or today.month
    year = year or today.year

    try:
        # import Transaction here to avoid potential circular imports
        from transactions.models import Transaction

        income_qs = Transaction.objects.filter(
            user=user,
            transaction_type="INCOME",
            date__month=month,
            date__year=year,
        )
        expense_qs = Transaction.objects.filter(
            user=user,
            transaction_type="EXPENSE",
            date__month=month,
            date__year=year,
        )

        income = _safe_aggregate(income_qs)
        expense = _safe_aggregate(expense_qs)

    except Exception as e:
        print("MONTHLY_SUMMARY DB ERROR:", e)
        income = 0
        expense = 0

    insights = []

    try:
        if expense > income:
            insights.append(
                f"Warning: You spent ₹{expense - income} more than your income this month."
            )
        else:
            insights.append(
                f"You saved ₹{income - expense} this month."
            )
    except Exception as e:
        print("MONTHLY_SUMMARY INSIGHT ERROR:", e)

    return {
        "income": income,
        "expense": expense,
        "savings": income - expense,
        "insights": insights,
    }


def category_breakdown(user, month=None, year=None):
    """
    Expense breakdown by category.
    Returns a queryset-like iterable of dicts with 'category' and 'total'.
    """
    today = date.today()
    month = month or today.month
    year = year or today.year

    try:
        from transactions.models import Transaction

        return (
            Transaction.objects.filter(
                user=user,
                transaction_type="EXPENSE",
                date__month=month,
                date__year=year,
            )
            .values("category")
            .annotate(total=Sum("amount"))
        )
    except Exception as e:
        print("CATEGORY_BREAKDOWN ERROR:", e)
        return []


def advanced_monthly_insights(user):
    """
    Slightly more verbose monthly insights including month name.
    """
    today = date.today()
    curr_month = today.month
    curr_year = today.year

    try:
        from transactions.models import Transaction

        income = _safe_aggregate(
            Transaction.objects.filter(
                user=user,
                transaction_type="INCOME",
                date__month=curr_month,
                date__year=curr_year,
            )
        )
        expense = _safe_aggregate(
            Transaction.objects.filter(
                user=user,
                transaction_type="EXPENSE",
                date__month=curr_month,
                date__year=curr_year,
            )
        )
    except Exception as e:
        print("ADVANCED_INSIGHTS DB ERROR:", e)
        income = 0
        expense = 0

    insights = []
    try:
        if expense > income:
            insights.append(f"Warning: Overspent ₹{expense - income}")
        else:
            insights.append(f"Saved ₹{income - expense}")
    except Exception as e:
        print("ADVANCED_INSIGHTS INSIGHT ERROR:", e)

    month_name = calendar.month_name[curr_month] if 1 <= curr_month <= 12 else ""

    return {
        "current_income": income,
        "current_expense": expense,
        "savings": income - expense,
        "insights": insights,
        "month_name": month_name,
    }


def generate_daily_insights(user):
    """
    Generate and persist daily insights using budget_alerts.
    Returns the list of messages created or found.
    """
    today = date.today()
    try:
        messages = budget_alerts(user)
    except Exception as e:
        print("BUDGET_ALERTS ERROR:", e)
        messages = []

    created = []
    for msg in messages:
        try:
            # Use get_or_create to avoid duplicates
            obj, was_created = Insight.objects.get_or_create(
                user=user,
                date=today,
                defaults={"text": msg},
            )
            if was_created:
                created.append(msg)
        except Exception as e:
            print("INSIGHT SAVE ERROR:", e)

    return messages
