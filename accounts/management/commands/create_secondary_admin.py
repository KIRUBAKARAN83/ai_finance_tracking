from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = "Create or promote secondary admin"

    def handle(self, *args, **kwargs):
        username = os.getenv("SECOND_ADMIN_USERNAME")
        email = os.getenv("SECOND_ADMIN_EMAIL")
        password = os.getenv("SECOND_ADMIN_PASSWORD")

        if not all([username, email, password]):
            self.stdout.write("❌ Secondary admin env vars missing")
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email}
        )

        if created:
            user.set_password(password)

        user.is_staff = True
        user.is_superuser = False  # ⚠️ keep limited
        user.save()

        self.stdout.write("✅ Secondary admin ready")
