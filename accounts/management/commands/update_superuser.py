from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Create or update one or more superusers using environment variables"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Support multiple superusers by comma-separated usernames
        usernames = os.environ.get("DJANGO_SUPERUSER_USERNAMES", "")
        if not usernames:
            self.stdout.write(self.style.WARNING("No DJANGO_SUPERUSER_USERNAMES set"))
            return

        for username in usernames.split(","):
            username = username.strip()
            email = os.environ.get(f"{username.upper()}_EMAIL", f"{username}@example.com")
            password = os.environ.get(f"{username.upper()}_PASSWORD", "changeme")

            user, created = User.objects.get_or_create(username=username)

            user.email = email
            user.is_superuser = True
            user.is_staff = True
            user.set_password(password)
            user.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' updated"))
