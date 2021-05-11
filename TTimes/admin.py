from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
# Register your models here.

admin.site.register(ParentCompanyModel)
admin.site.register(StaffModel)
admin.site.register(AttendanceModel)

@admin.register(ChildCompanyModel)
class AdminChildCompanyModel(UserAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('name', 'email', 'is_staff')
    search_fields = ('name', 'email')
    filter_horizontal = ()