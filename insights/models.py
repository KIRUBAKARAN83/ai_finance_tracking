from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Insight(models.Model):
    """
    Stores AI-generated financial insights per user per day.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="insights"
    )

    text = models.TextField(
        help_text="AI-generated financial insight"
    )

    date = models.DateField(
        default=now,
        help_text="Date this insight applies to"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        # ✅ SAFE unique constraint (NO TextField indexing)
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date"],
                name="unique_insight_per_user_per_day"
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"Insight({self.user.username} | {self.date})"
