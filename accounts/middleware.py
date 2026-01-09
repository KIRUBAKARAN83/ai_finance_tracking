# accounts/middleware.py
from django.utils.timezone import now
from django.db import DatabaseError
from django.apps import apps
import logging

logger = logging.getLogger(__name__)

class ActiveUserMiddleware:
    """
    Middleware that updates a UserActivity.last_seen timestamp for authenticated users.

    Defensive behavior:
    - Avoids DB access during migrations or when the auth app isn't ready.
    - Catches broad database errors and logs them instead of raising.
    - Skips update for anonymous users or when request has no user attribute.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Guard: ensure request has a user and it's authenticated
        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            return response

        # Guard: ensure accounts app models are ready to avoid AppRegistryNotReady
        if not apps.ready:
            return response

        try:
            # Import inside try to avoid import-time circular issues
            from accounts.models import UserActivity
            # update_or_create is safe; wrap DB access in try/except
            UserActivity.objects.update_or_create(
                user=user,
                defaults={"last_seen": now()}
            )
        except DatabaseError as db_err:
            # Database not available (migrations, connection issues) — log and continue
            logger.debug("ActiveUserMiddleware DB error: %s", db_err)
        except Exception as exc:
            # Catch-all to avoid any unexpected middleware crash
            logger.exception("ActiveUserMiddleware unexpected error: %s", exc)

        return response
