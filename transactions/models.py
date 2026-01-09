# transactions/models.py
from decimal import Decimal
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

# Try to import the AI category predictor; fall back to a safe stub if unavailable.
try:
    from insights.ai_engine import predict_category  # may raise ImportError in some environments
except Exception:
    def predict_category(text: str) -> str:
        # Safe fallback: don't raise during model save
        return "Uncategorized"


class Transaction(models.Model):
    EXPENSE = "EXPENSE"
    INCOME = "INCOME"

    TYPE_CHOICES = [
        (EXPENSE, "Expense"),
        (INCOME, "Income"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])
    category = models.CharField(max_length=50, blank=True)
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date = models.DateField(default=date.today)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-date", "-id"]
        indexes = [
            models.Index(fields=["user", "date"]),
            models.Index(fields=["user", "transaction_type"]),
        ]

    def save(self, *args, **kwargs):
        """
        - If category is empty, attempt to predict it from the note.
        - Normalize category to Title Case and strip whitespace.
        - Wrap AI call in try/except to avoid raising during save.
        """
        # Only attempt prediction if category is empty and note has content
        if not self.category:
            try:
                predicted = predict_category(self.note or "")
                # Ensure we have a non-empty string
                if predicted:
                    self.category = str(predicted)
                else:
                    self.category = "Uncategorized"
            except Exception:
                # If the predictor fails for any reason, fall back safely
                self.category = "Uncategorized"

        # Normalize category for consistent matching with budgets
        try:
            self.category = self.category.strip().title()
        except Exception:
            # Defensive fallback if category is not a string
            self.category = "Uncategorized"

        # Ensure amount is non-negative (validator will enforce on full_clean/migrate)
        if self.amount is None:
            self.amount = Decimal("0.00")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} ₹{self.amount} — {self.category}"


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")
    category = models.CharField(max_length=50)
    limit = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])

    class Meta:
        unique_together = ("user", "category")
        ordering = ["category"]

    def save(self, *args, **kwargs):
        # Normalize category to Title Case
        try:
            self.category = self.category.strip().title()
        except Exception:
            self.category = str(self.category or "").strip().title()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category} – ₹{self.limit}"


class RecurringTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recurring_transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])
    category = models.CharField(max_length=50)
    transaction_type = models.CharField(max_length=10, choices=Transaction.TYPE_CHOICES)
    day_of_month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])

    class Meta:
        ordering = ["user", "day_of_month"]

    def save(self, *args, **kwargs):
        try:
            self.category = self.category.strip().title()
        except Exception:
            self.category = str(self.category or "").strip().title()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category} ({self.transaction_type}) on day {self.day_of_month}"
