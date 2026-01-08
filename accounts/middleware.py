from django.utils.timezone import now
from django.db.utils import OperationalError

class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            try:
                from accounts.models import UserActivity
                UserActivity.objects.update_or_create(
                    user=request.user,
                    defaults={"last_seen": now()}
                )
            except OperationalError:
                pass  # table not migrated yet

        return response
