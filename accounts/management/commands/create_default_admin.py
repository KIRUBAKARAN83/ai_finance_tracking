from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Create default admin if not exists"

    def handle(self, *args, **kwargs):
        username = "admin"
        email = "admin@example.com"
        password = "Admin@123"  # 🔥 change later after login

        if User.objects.filter(username=username).exists():
            self.stdout.write("ℹ️ Admin already exists")
            return

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write("✅ Default admin created")
