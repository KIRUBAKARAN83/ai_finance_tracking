# insights/budget_suggest.py
from decimal import Decimal
from datetime import date, timedelta
from django.db.models import Avg
from transactions.models import Transaction


def suggest_budgets(user):
    last_3_months = date.today() - timedelta(days=90)

    qs = (
        Transaction.objects
        .filter(
            user=user,
            transaction_type="EXPENSE",
            date__gte=last_3_months
        )
        .values("category")
        .annotate(avg_spend=Avg("amount"))
    )

    suggestions = []

    for row in qs:
        avg_spend = row["avg_spend"]

        if avg_spend is None:
            continue

        # Ensure Decimal math
        avg_spend = Decimal(avg_spend)

        # Add 20% buffer safely
        suggested = (avg_spend * Decimal("1.20")).quantize(
            Decimal("0.01")
        )

        suggestions.append({
            "category": row["category"].strip().title(),  # normalize
            "suggested_limit": suggested
        })

    return suggestions
