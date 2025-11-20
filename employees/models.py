from django.db import models
from django.contrib.auth.models import User

# 1. Department and Designation
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Designation(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


# 2. Employee Profile
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    emp_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True) 
    phone = models.CharField(max_length=20)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    date_joined = models.DateField()
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# 3. Attendance & Leave Tracking
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.employee.first_name} - {self.date} ({self.status})"


class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ], default='Pending')

    def __str__(self):
        return f"{self.employee.first_name} ({self.status})"


# 4. Payroll Management
class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    provident_fund = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    month = models.CharField(max_length=20)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.net_salary = (self.basic_salary + self.hra + self.allowances) - (self.provident_fund + self.tax)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.first_name} - {self.month}"
    

from django.db import models
from django.contrib.auth.models import User

class EmployeeLoginLogout(models.Model):
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.user.username} - Login: {self.login_time} Logout: {self.logout_time}"


from django.db import models
from .models import Employee  # Import the Employee model

class Meeting(models.Model):
    title = models.CharField(max_length=200)
    datetime = models.DateTimeField()
    details = models.TextField()
    meeting_link = models.URLField(blank=True, null=True)  # NEW FIELD
    employees = models.ManyToManyField(Employee, related_name='meetings')  # Many-to-many relation
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True, null=True)  # Optional field

    def __str__(self):
        return self.title

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}"

class WorkFromHome(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.first_name} - {self.date}"

from django.db import models
from django.contrib.auth.models import User
import random

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))

