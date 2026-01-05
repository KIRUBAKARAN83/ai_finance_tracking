from django.core.management.base import BaseCommand
from insights.cron import generate_daily_insights

class Command(BaseCommand):
    help = "Generate daily AI insights"

    def handle(self, *args, **kwargs):
        generate_daily_insights()
        self.stdout.write("✅ AI insights generated")
