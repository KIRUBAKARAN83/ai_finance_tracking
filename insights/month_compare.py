from django.db.models import Sum
from transactions.models import Transaction
from datetime import date


def month_comparison(user):
    today = date.today()
    curr_month = today.month
    prev_month = curr_month - 1 or 12
    prev_year = today.year if curr_month != 1 else today.year - 1

    curr_exp = Transaction.objects.filter(
        user=user,
        transaction_type="EXPENSE",
        date__month=curr_month,
        date__year=today.year
    ).aggregate(total=Sum("amount"))["total"] or 0

    prev_exp = Transaction.objects.filter(
        user=user,
        transaction_type="EXPENSE",
        date__month=prev_month,
        date__year=prev_year
    ).aggregate(total=Sum("amount"))["total"] or 0

    if prev_exp == 0:
        return {
            "status": "no-data",
            "message": "No previous month data available",
            "percent": 0,
            "direction": "neutral",
            "color": "secondary",
        }

    diff = curr_exp - prev_exp
    percent = round((diff / prev_exp) * 100, 1)

    if percent > 30:
        return {
            "status": "warning",
            "message": f"Expenses increased by {percent}%",
            "percent": percent,
            "direction": "up",
            "color": "danger",
        }
    elif percent < -10:
        return {
            "status": "good",
            "message": f"Expenses reduced by {abs(percent)}%",
            "percent": abs(percent),
            "direction": "down",
            "color": "success",
        }
    else:
        return {
            "status": "stable",
            "message": "Spending is stable compared to last month",
            "percent": percent,
            "direction": "flat",
            "color": "primary",
        }
