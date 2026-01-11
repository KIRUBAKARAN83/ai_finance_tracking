# ai_finance_tracker/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin site
    path("admin/", admin.site.urls),

    # Accounts: include your custom app URLs
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),

    # Django’s built-in auth views (login, logout, password reset, etc.)
    path("accounts/", include("django.contrib.auth.urls")),

    # Transactions app (dashboard at /)
    path("", include(("transactions.urls", "transactions"), namespace="transactions")),
]
