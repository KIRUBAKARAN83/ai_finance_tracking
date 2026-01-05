from django.utils.timezone import now
from .models import UserActivity

class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            UserActivity.objects.update_or_create(
                user=request.user,
                defaults={"last_seen": now()}
            )
        return self.get_response(request)
