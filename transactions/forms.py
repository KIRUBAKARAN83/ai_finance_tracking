from django import forms
from .models import Transaction, Budget


# ============================
# TRANSACTION FORM
# ============================
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["amount", "category", "transaction_type", "date", "note"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "category": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Optional (AI will auto-fill if empty)"
            }),
        }


# ============================
# BUDGET FORM
# ============================
class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["category", "limit"]   # ✅ FIXED FIELD
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
