from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Task

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_active', 'is_deactivated', 'missed_tasks_count')
    list_filter = ('role', 'is_deactivated', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'is_deactivated', 'missed_tasks_count')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'is_deactivated', 'missed_tasks_count')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Task)

