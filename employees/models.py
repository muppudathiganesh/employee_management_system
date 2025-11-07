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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.employee.username} - Login: {self.login_time} Logout: {self.logout_time}"
