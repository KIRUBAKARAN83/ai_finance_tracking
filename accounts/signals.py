from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, UserActivity


@receiver(post_save, sender=User)
def create_related_models(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
        UserActivity.objects.get_or_create(user=instance)
