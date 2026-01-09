from decimal import Decimal
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Transaction, Budget


# ============================
# TRANSACTION FORM
# ============================
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["amount", "category", "transaction_type", "date", "note"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "category": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Optional (AI will auto-fill if empty)"
            }),
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "note": forms.TextInput(attrs={"class": "form-control", "placeholder": "Optional note"}),
            "transaction_type": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount is None:
            raise ValidationError("Amount is required.")
        if amount < Decimal("0.00"):
            raise ValidationError("Amount must be non-negative.")
        return amount

    def clean_date(self):
        dt = self.cleaned_data.get("date")
        if dt is None:
            return timezone.localdate()
        return dt

    def clean_category(self):
        cat = self.cleaned_data.get("category") or ""
        return cat.strip().title()


# ============================
# BUDGET FORM
# ============================
class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["category", "limit"]
        widgets = {
            "category": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. Food, Travel"
            }),
            "limit": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "Monthly limit (₹)"
            }),
        }

    def clean_limit(self):
        limit = self.cleaned_data.get("limit")
        if limit is None:
            raise ValidationError("Limit is required.")
        if limit < Decimal("0.00"):
            raise ValidationError("Limit must be non-negative.")
        return limit

    def clean_category(self):
        cat = self.cleaned_data.get("category") or ""
        return cat.strip().title()
