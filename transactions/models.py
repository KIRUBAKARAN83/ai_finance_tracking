from django.db import models
from django.contrib.auth.models import User
from insights.ai_engine import predict_category


# ============================
# TRANSACTION
# ============================
class Transaction(models.Model):
    EXPENSE = "EXPENSE"
    INCOME = "INCOME"

    TYPE_CHOICES = [
        (EXPENSE, "Expense"),
        (INCOME, "Income"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # normalized category
    category = models.CharField(max_length=50, blank=True)

    transaction_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES
    )

    date = models.DateField()
    note = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        # AI category if empty
        if not self.category:
            self.category = predict_category(self.note)

        # normalize category for budget matching
        self.category = self.category.strip().title()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} ₹{self.amount}"


# ============================
# BUDGET (SINGLE SOURCE OF TRUTH)
# ============================
class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # must match Transaction.category
    category = models.CharField(max_length=50)

    limit = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # normalize category
        self.category = self.category.strip().title()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category} – ₹{self.limit}"


# ============================
# RECURRING TRANSACTION
# ============================
class RecurringTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    transaction_type = models.CharField(max_length=10)
    day_of_month = models.IntegerField()

    def save(self, *args, **kwargs):
        self.category = self.category.strip().title()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category} ({self.transaction_type})"
    


   

