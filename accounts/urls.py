
from django.urls import path, include
from .views import register, profile

urlpatterns = [
    path("register/", register, name="register"),

    # ✅ ALLAUTH HANDLES LOGIN
    path("", include("allauth.urls")),

    path("profile/", profile, name="profile"),
]
