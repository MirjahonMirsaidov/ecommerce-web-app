from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from .models import *


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['name']
    fieldsets = (
        (None, {'fields': ('name', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important data'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'password1', 'password2')
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Region)
admin.site.register(District)
admin.site.register(Address)
