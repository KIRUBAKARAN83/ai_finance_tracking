# insights/chat_engine.py

import os
from datetime import date
from django.db.models import Sum
from django.db.utils import OperationalError

from groq import Groq

from transactions.models import Transaction, Budget


# ======================================================
# NON-STREAMING CHAT (SAFE)
# ======================================================
def finance_chat(user, message):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "⚠️ AI service not configured."

    try:
        client = Groq(api_key=api_key)
        today = date.today()

        income = (
            Transaction.objects.filter(
                user=user,
                transaction_type="INCOME",
                date__month=today.month,
                date__year=today.year,
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )

        expense = (
            Transaction.objects.filter(
                user=user,
                transaction_type="EXPENSE",
                date__month=today.month,
                date__year=today.year,
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )

        budgets = list(
            Budget.objects.filter(user=user)
            .values("category", "limit")
        )

        prompt = f"""
You are a personal finance assistant.
Use ONLY the data below.

Income: ₹{income}
Expense: ₹{expense}
Budgets: {budgets}

User question:
{message}

Answer briefly and clearly.
"""

        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=200,
        )

        return res.choices[0].message.content.strip()

    except Exception as e:
        print("GROQ ERROR:", e)
        return "⚠️ AI service temporarily unavailable."


# ======================================================
# STREAMING CHAT (SAFE FOR RENDER)
# ======================================================
def finance_chat_stream(user, message):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        yield "⚠️ AI service not configured."
        return

    try:
        client = Groq(api_key=api_key)
        today = date.today()

        income = (
            Transaction.objects.filter(
                user=user,
                transaction_type="INCOME",
                date__month=today.month,
                date__year=today.year,
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )

        expense = (
            Transaction.objects.filter(
                user=user,
                transaction_type="EXPENSE",
                date__month=today.month,
                date__year=today.year,
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )

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
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=200,
            stream=True,
        )

        full_reply = ""

        for chunk in stream:
            token = chunk.choices[0].delta.content
            if token:
                full_reply += token
                yield token

        # --------------------------------------------------
        # SAVE INSIGHT (FAIL-SAFE)
        # --------------------------------------------------
        try:
            from insights.models import Insight

            Insight.objects.get_or_create(
                user=user,
                date=today,
                defaults={"text": full_reply.strip()},
            )
        except OperationalError:
            # table not migrated yet – ignore safely
            pass

    except Exception as e:
        print("GROQ STREAM ERROR:", e)
        yield "\n⚠️ AI service unavailable."
