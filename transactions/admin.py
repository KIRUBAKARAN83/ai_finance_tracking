from django.contrib import admin
from .models import Transaction, Budget


@admin.register(Transaction)


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'transaction_type',
        'category',
        'amount',
        'date',
    )
    list_filter = (
        'transaction_type',
        'category',
        'date',
    )
    search_fields = (
        'note',
        'category',
    )
    ordering = ('-date',)



