# accounts/models.py
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    monthly_income = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="User's expected monthly income in INR",
    )

    def __str__(self):
        return f"{self.user.username} Profile"


class UserActivity(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="activity",
    )
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} activity"

# Signals: create Profile and UserActivity automatically when a User is created
@receiver(post_save, sender=User)
def create_user_related_models(sender, instance, created, **kwargs):
    if created:
        # Create profile and activity safely
        Profile.objects.get_or_create(user=instance)
        UserActivity.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_related_models(sender, instance, **kwargs):
    # Ensure related objects exist and are saved when user is saved
    try:
        if hasattr(instance, "profile"):
            instance.profile.save()
    except Exception:
        # avoid raising during user save; log in real app
        pass

    try:
        if hasattr(instance, "activity"):
            instance.activity.save()
    except Exception:
        pass
