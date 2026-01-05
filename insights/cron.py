from datetime import date
from insights.budget_alerts import budget_alerts
from insights.health_score import financial_health_score
from django.contrib.auth.models import User
from insights.models import Insight  # create this model

def generate_daily_insights():
    today = date.today()

    for user in User.objects.filter(is_active=True):
        alerts = budget_alerts(user)
        health = financial_health_score(user)

        messages = alerts + health.get("messages", [])

        for msg in messages:
            Insight.objects.get_or_create(
                user=user,
                date=today,
                text=msg
            )
