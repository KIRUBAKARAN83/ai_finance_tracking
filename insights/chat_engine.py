# insights/chat_engine.py
import os
from datetime import date
from django.db.models import Sum
from groq import Groq
from transactions.models import Transaction, Budget

def finance_chat(user, message):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "⚠️ GROQ_API_KEY not set."

    try:
        client = Groq(api_key=api_key)
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

        budgets = list(
            Budget.objects.filter(user=user)
            .values("category", "limit")
        )

        prompt = f"""
You are a finance assistant.
Use ONLY the data below.

Income: ₹{income}
Expense: ₹{expense}
Budgets: {budgets}

User question: {message}

Answer briefly and clearly.
"""

        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
        )

        return res.choices[0].message.content.strip()

    except Exception as e:
        print("GROQ ERROR:", e)
        return "⚠️ AI service temporarily unavailable."
    


    # insights/chat_engine.py

import os
from datetime import date
from django.db.models import Sum
from groq import Groq

from transactions.models import Transaction, Budget
from insights.models import Insight

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def finance_chat_stream(user, message):
    today = date.today()

    income = Transaction.objects.filter(
        user=user,
        transaction_type="INCOME",
        date__month=today.month,
        date__year=today.year,
    ).aggregate(total=Sum("amount"))["total"] or 0

    expense = Transaction.objects.filter(
        user=user,
        transaction_type="EXPENSE",
        date__month=today.month,
        date__year=today.year,
    ).aggregate(total=Sum("amount"))["total"] or 0

    budgets = list(
        Budget.objects.filter(user=user)
        .values("category", "limit")
    )

    prompt = f"""
You are a personal finance assistant.
Use ONLY this data.

Income: ₹{income}
Expense: ₹{expense}
Budgets: {budgets}

User question:
{message}

Give short, clear advice.
"""

    stream = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=150,
        stream=True,
    )

    full_reply = ""

    for chunk in stream:
        if chunk.choices[0].delta.content:
            token = chunk.choices[0].delta.content
            full_reply += token
            yield token

    # save final insight
    Insight.objects.get_or_create(
        user=user,
        date=today,
        text=full_reply.strip(),
    )

