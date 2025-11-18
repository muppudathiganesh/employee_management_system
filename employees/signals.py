from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import EmployeeLoginLogout
from django.utils import timezone

@receiver(user_logged_in)
def log_employee_login(sender, request, user, **kwargs):
    if hasattr(user, "employee"):
        EmployeeLoginLogout.objects.create(
            employee=user.employee,
            login_time=timezone.now()
        )

@receiver(user_logged_out)
def log_employee_logout(sender, request, user, **kwargs):
    if hasattr(user, "employee"):
        last_entry = EmployeeLoginLogout.objects.filter(
            employee=user.employee,
            logout_time__isnull=True
        ).last()
        if last_entry:
            last_entry.logout_time = timezone.now()
            last_entry.save()



from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Employee

@receiver(post_save, sender=User)
def create_employee_for_user(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'employee'):
        Employee.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name
        )

