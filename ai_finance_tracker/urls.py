from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth
  
    path("accounts/", include("accounts.urls")),

    # Transactions app (namespaced)
    path("", include(("transactions.urls", "transactions"), namespace="transactions")),
    path("accounts/", include("allauth.urls")),

]
