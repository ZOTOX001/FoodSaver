from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_verified', 'trust_score')
    list_filter = ('role', 'is_verified')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'is_verified', 'trust_score', 'latitude', 'longitude', 'restaurant_license', 'ngo_registration', 'institution_name')}),
    )

admin.site.register(User, CustomUserAdmin)
