from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Create default superuser if not exists"

    def handle(self, *args, **kwargs):
        username = "kiruba_karan"
        email = "dhayalankiruba17@gmail.com"
        password = "kiruba@123"

        if User.objects.filter(username=username).exists():
            self.stdout.write("ℹ️ Superuser already exists")
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write("✅ Superuser created successfully")
