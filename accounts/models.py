from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    monthly_income = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0  # ✅ CRITICAL FIX
    )

    def __str__(self):
        return self.user.username


class UserActivity(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="activity"
    )
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} (last seen)"
