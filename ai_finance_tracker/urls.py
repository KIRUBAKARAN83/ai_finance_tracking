from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Authentication (Django + Allauth)
   
    path("accounts/", include("accounts.urls")),

    # Transactions app (dashboard at /)
    path("", include("transactions.urls")),
]
