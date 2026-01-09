from django.contrib import admin
from .models import Profile, UserActivity


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "monthly_income",
    )
    search_fields = (
        "user__username",
    )


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ("user", "last_seen")
    search_fields = ("user__username",)
    readonly_fields = ("last_seen",)
