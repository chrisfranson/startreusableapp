"""
Models for ${app_name} with OAuth2/user scoping support.

All models include a user foreign key for multi-tenant data isolation.
"""
from django.conf import settings
from django.db import models


class ExampleModel(models.Model):
    """
    Example model with user scoping.

    Customize this model for your app's needs.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='${app_name}_examples',
        help_text='Owner of this record'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"{self.name} ({self.user.username})"
