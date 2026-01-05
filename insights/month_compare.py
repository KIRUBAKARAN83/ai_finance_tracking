from django.db.models import Sum
from transactions.models import Transaction
from datetime import date

def month_comparison(user):
    today = date.today()
    curr = today.month
    prev = curr - 1 or 12

    curr_exp = Transaction.objects.filter(
        user=user,
        transaction_type="EXPENSE",
        date__month=curr
    ).aggregate(total=Sum("amount"))["total"] or 0

    prev_exp = Transaction.objects.filter(
        user=user,
        transaction_type="EXPENSE",
        date__month=prev
    ).aggregate(total=Sum("amount"))["total"] or 0

    if prev_exp == 0:
        return "No previous month data."

    diff = curr_exp - prev_exp
    percent = (diff / prev_exp) * 100

    if percent > 30:
        return f"⚠ Expenses increased by {percent:.1f}% compared to last month."
    elif percent < -10:
        return f"✅ Expenses reduced by {abs(percent):.1f}%."
    else:
        return "Spending is stable compared to last month."
