# transactions/management/commands/update_superuser.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Create or update a superuser using environment variables"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "changeme")

        user, created = User.objects.get_or_create(username=username, defaults={
            "email": email,
            "is_superuser": True,
            "is_staff": True,
        })

        user.email = email
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)   # ✅ applies password from environment
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' updated"))
