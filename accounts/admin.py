from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.unregister(User)


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_roles', 'is_staff', 'is_active')
    list_filter = ('groups', 'is_staff', 'is_active')

    def get_roles(self, obj):
        return ', '.join([g.name for g in obj.groups.all()]) or 'No role'
    get_roles.short_description = 'Roles'


admin.site.register(User, CustomUserAdmin)
