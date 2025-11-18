from django.contrib import admin
from .models import Department, Designation, Employee, Attendance, Leave, Payroll, Meeting, EmployeeLoginLogout

admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(Leave)
admin.site.register(Payroll)
admin.site.register(Meeting)

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

@admin.register(EmployeeLoginLogout)
class EmployeeLoginLogoutAdmin(admin.ModelAdmin):
    list_display = ('employee', 'login_time', 'logout_time')
