# ai_finance_tracker/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Accounts app (register, profile, etc.)
    path("accounts/", include("accounts.urls")),

    # Django built-in auth (login, logout, password reset)
    path("accounts/", include("django.contrib.auth.urls")),

    # Main app (dashboard at /)
    path("", include(("transactions.urls", "transactions"), namespace="transactions")),
]
