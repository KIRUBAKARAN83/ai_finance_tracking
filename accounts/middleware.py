# accounts/middleware.py
from django.utils.timezone import now
from django.db import OperationalError, IntegrityError
from .models import UserActivity


class ActiveUserMiddleware:
    """
    Safely track last seen users.
    - No writes for anonymous users
    - Fail-safe (never crashes requests)
    - Skips static/admin paths
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # ✅ Only after response
        user = getattr(request, "user", None)

        if (
            user
            and user.is_authenticated
            and not request.path.startswith("/static/")
            and not request.path.startswith("/admin/")
        ):
            try:
                UserActivity.objects.update_or_create(
                    user=user,
                    defaults={"last_seen": now()},
                )
            except (OperationalError, IntegrityError):
                # ❌ NEVER break production requests
                pass

        return response
