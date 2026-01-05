from django.core.management.base import BaseCommand
from datetime import date
from transactions.models import RecurringTransaction, Transaction

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        today = date.today()
        recs = RecurringTransaction.objects.filter(day_of_month=today.day)

        for r in recs:
            Transaction.objects.create(
                user=r.user,
                amount=r.amount,
                category=r.category,
                transaction_type=r.transaction_type,
                date=today,
                note="Auto recurring entry"
            )
