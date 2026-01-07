from django.contrib import admin
from django.urls import path, include
from transactions import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Django’s built-in auth views (login, logout, password reset, etc.)
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("accounts.urls")),

    # Transactions app with namespace
    path("", include(("transactions.urls", "transactions"), namespace="transactions")),

    # Direct view route (optional, but usually better inside transactions/urls.py)
    path("transactions/", views.all_transactions, name="all_transactions"),
]
