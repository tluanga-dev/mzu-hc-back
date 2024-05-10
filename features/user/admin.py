# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('user_name',)}), 
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','user_id', 'user_name', 'password1', 'password2'), 
        }),
    )
    list_display = ['email', 'user_name', 'user_id', 'is_staff', 'is_active']
    search_fields = ('email', 'user_name', 'user_id')
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)
