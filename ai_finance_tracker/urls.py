# ai_finance_tracker/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin site
    path("admin/", admin.site.urls),

    # Accounts: include both custom app URLs and Django's built-in auth views
    path(
        "accounts/",
        include(
            [
                path("", include(("accounts.urls", "accounts"))),
                path("", include("django.contrib.auth.urls")),
            ]
        ),
    ),

    # Transactions app (dashboard at /)
    path("", include(("transactions.urls", "transactions"), namespace="transactions")),
]
