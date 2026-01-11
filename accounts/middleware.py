# accounts/middleware.py
from django.utils.timezone import now
from django.db.utils import OperationalError, ProgrammingError

try:
    from .models import UserActivity
except Exception:
    UserActivity = None


class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if (
            UserActivity
            and hasattr(request, "user")
            and request.user.is_authenticated
        ):
            try:
                UserActivity.objects.update_or_create(
                    user=request.user,
                    defaults={"last_seen": now()},
                )
            except (OperationalError, ProgrammingError) as e:
                # Happens on Render when table/migrations are missing
                print("ActiveUserMiddleware skipped:", e)

        return response
