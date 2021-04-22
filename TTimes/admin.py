from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(ParentCompanyModel)
admin.site.register(ChildCompanyModel)
admin.site.register(StaffModel)
admin.site.register(AttendanceModel)