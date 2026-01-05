import matplotlib
matplotlib.use("Agg")  # IMPORTANT (no GUI)

import matplotlib.pyplot as plt
from django.http import HttpResponse
from .services import category_breakdown
from datetime import date

def expense_category_chart(request):
    today = date.today()
    df = category_breakdown(request.user, today.month, today.year)

    if df.empty:
        return HttpResponse("No data")

    plt.figure(figsize=(6,4))
    plt.bar(df["category"], df["total"])
    plt.title("Expense by Category (₹)")
    plt.xlabel("Category")
    plt.ylabel("Amount (₹)")
    plt.tight_layout()

    response = HttpResponse(content_type="image/png")
    plt.savefig(response, format="png")
    plt.close()

    return response
