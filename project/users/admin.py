from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'cardId', 'is_staff', 'is_active')  # Add 'cardId' to list_display
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'cardId')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'cardId', 'is_staff', 'is_active'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
