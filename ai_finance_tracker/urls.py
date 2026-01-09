from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin site
    path("admin/", admin.site.urls),

    # Authentication (custom + built-in)
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("accounts/", include("django.contrib.auth.urls")),

    # Transactions app (dashboard at /)
    path("", include(("transactions.urls", "transactions"), namespace="transactions")),
]
