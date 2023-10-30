"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ["id"]
    list_display = ["email", "first_name", "last_name", "is_staff"]
    fieldsets = (
        (None, {"fields": ("password", "first_name", "last_name")}),
        (_("Permissions"), {"fields": ("is_active",
                                       "is_staff",
                                       "is_superuser")}),
        (_("Important dates"), {"fields": ("date_joined", "last_login",)}),
    )
    readonly_fields = ["date_joined", "last_login"]

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "password1",
                "password2",
                "first_name",
                "last_name",
                "is_active",
                "is_staff",
                "is_superuser",
            ),
        }),
    )


class ProductAdmin(admin.ModelAdmin):
    """Customize product model for admin."""
    ordering = ["id"]
    list_display = ["title", "category", "price"]
    search_fields = ["title"]
    actions = ["change_category"]
    list_editable = ["category", "price"]

    def change_category(self, request, queryset):
        """Change the category of the product."""
        queryset.update(category="default")


admin.site.site_header = "ABC E-Commerce Shop"
admin.site.site_title = "ABC Shop"
admin.site.index_title = "ABC Admin E-Com Shop"

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Profile)
admin.site.register(models.Order)
