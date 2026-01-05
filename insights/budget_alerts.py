# insights/budget_alerts.py
from decimal import Decimal
from datetime import date
from django.db.models import Sum
from transactions.models import Transaction, Budget


def budget_alerts(user):
    today = date.today()
    alerts = []

    budgets = Budget.objects.filter(user=user)

    for budget in budgets:
        spent = (
            Transaction.objects.filter(
                user=user,
                transaction_type="EXPENSE",
                category__iexact=budget.category.strip(),
                date__month=today.month,
                date__year=today.year
            )
            .aggregate(total=Sum("amount"))["total"]
        )

        spent = spent if spent is not None else Decimal("0")
        limit = budget.limit if budget.limit is not None else Decimal("0")

        if limit <= 0:
            continue  # skip invalid budgets

        percent_used = (spent / limit) * Decimal("100")

        if percent_used >= 100:
            alerts.append(
                f"🚨 Budget exceeded for {budget.category}. "
                f"Limit ₹{limit}, spent ₹{spent}."
            )
        elif percent_used >= 80:
            alerts.append(
                f"⚠️ You have used {int(percent_used)}% of your "
                f"{budget.category} budget (₹{spent} / ₹{limit})."
            )

    return alerts
