from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import EmployeeLoginLogout
from django.utils import timezone

@receiver(user_logged_in)
def log_employee_login(sender, request, user, **kwargs):
    EmployeeLoginLogout.objects.create(employee=user, login_time=timezone.now())

@receiver(user_logged_out)
def log_employee_logout(sender, request, user, **kwargs):
    # Get the latest login record for today
    last_record = EmployeeLoginLogout.objects.filter(employee=user, logout_time__isnull=True).last()
    if last_record:
        last_record.logout_time = timezone.now()
        last_record.save()
