# insights/budget_progress.py
from decimal import Decimal
from datetime import date
from django.db.models import Sum
from transactions.models import Transaction, Budget


def budget_progress(user):
    progress = []
    today = date.today()

    budgets = Budget.objects.filter(user=user)

    for budget in budgets:
        spent = (
            Transaction.objects.filter(
                user=user,
                transaction_type="EXPENSE",
                category__iexact=budget.category.strip(),  # ✅ FIX
                date__month=today.month,                   # ✅ FIX
                date__year=today.year                      # ✅ FIX
            )
            .aggregate(total=Sum("amount"))["total"]
        )

        spent = spent if spent is not None else Decimal("0")
        limit = budget.limit if budget.limit is not None else Decimal("0")

        if limit > 0:
            percent = (spent / limit) * Decimal("100")
        else:
            percent = Decimal("0")

        progress.append({
            "category": budget.category,
            "spent": spent.quantize(Decimal("0.01")),
            "limit": limit.quantize(Decimal("0.01")),
            "percent": min(int(percent), 100),
        })

    return progress
