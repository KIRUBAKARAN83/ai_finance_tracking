

from django.contrib import admin
from django.urls import path, include
from transactions import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("accounts.urls")),
    path("", include("transactions.urls"),namespace="transactions")),  # MUST EXIST
    path("", include("transactions.urls", "transactions"), namespace="transactions"),
    path("transactions/", views.all_transactions, name="all_transactions"),
]

