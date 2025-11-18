from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import Employee, Department, Designation, Payroll, Attendance, Leave
import csv
from reportlab.pdfgen import canvas

# ------------------ Employee List ------------------
def employee_list(request):
    q = request.GET.get('q', '')  # search query
    if q:
        employees = Employee.objects.filter(first_name__icontains=q)
    else:
        employees = Employee.objects.all()

    return render(request, 'employees/employee_list.html', {'employees': employees, 'q': q})
# ------------------ Add Employee ------------------
from django.shortcuts import render, redirect
from .models import Employee, Department, Designation
from datetime import date

def add_employee(request):
    if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')  
        department_name = request.POST.get('department')
        designation_name = request.POST.get('designation')
       
        department, _ = Department.objects.get_or_create(name=department_name)
        designation, _ = Designation.objects.get_or_create(title=designation_name)

        Employee.objects.create(
            emp_id=emp_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            department=department,
            designation=designation,
            date_joined=date.today()   # ✅ Auto-fill current date
        )
        return redirect('employee_list')

    departments = Department.objects.all()
    designations = Designation.objects.all()
    return render(request, 'employees/add_employee.html', {
        'departments': departments,
        'designations': designations
    })

# ------------------ Edit Employee ------------------
def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    departments = Department.objects.all()
    designations = Designation.objects.all()

    if request.method == 'POST':
        employee.first_name = request.POST.get('first_name')
        employee.last_name = request.POST.get('last_name')
        employee.department = Department.objects.get(id=request.POST.get('department'))
        employee.designation = Designation.objects.get(id=request.POST.get('designation'))
        employee.save()
        messages.success(request, "Employee updated successfully!")
        return redirect('employee_list')

    return render(request, 'employees/edit_employee.html', {
        'employee': employee,
        'departments': departments,
        'designations': designations
    })


# ------------------ Delete Employee ------------------
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        employee.delete()
        messages.warning(request, "Employee deleted successfully!")
        return redirect('employee_list')
    return render(request, 'employees/confirm_delete.html', {'employee': employee})


# dashboard--------------------------------------

from django.shortcuts import render
from datetime import date
from .models import Employee, Department, Leave, Attendance  # Ensure Attendance model exists

def dashboard(request):
    today = date.today()

    total_employees = Employee.objects.count()
    on_leave_today = Leave.objects.filter(
        status='Approved',
        start_date__lte=today,
        end_date__gte=today
    ).count()

    present_today = Attendance.objects.filter(
        date=today, status='Present'
    ).count()

    absent_today = max(total_employees - (present_today + on_leave_today), 0)
    total_departments = Department.objects.count()
    pending_approvals = Leave.objects.filter(status='Pending').count()

    return render(request, 'employees/home.html', {
        'total_employees': total_employees,
        'on_leave_today': on_leave_today,
        'total_departments': total_departments,
        'pending_approvals': pending_approvals,
        'present_today': present_today,
        'absent_today': absent_today,
        'leave_today': on_leave_today,
    })

# ---------------------departments------------
from django.shortcuts import render
from .models import Department

def view_departments(request):
    departments = Department.objects.all()
    return render(request, 'employees/departments.html', {'departments': departments})
# add department---------------------------------s
from django.shortcuts import render, redirect
from .models import Department

def add_department(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Department.objects.get_or_create(name=name)
            return redirect('view_departments')
    return render(request, 'employees/add_department.html')

# -----------------------leave---------
from django.shortcuts import render
from .models import Employee, Attendance, Leave

def employee_list(request):
    employees = Employee.objects.all()
    attendance_data = Attendance.objects.all()
    leave_data = Leave.objects.all()

    return render(request, 'employees/employee_list.html', {
        'employees': employees,
        'attendance_data': attendance_data,
        'leave_data': leave_data,
    })





# ---------------------attendance------------
from django.shortcuts import render
from .models import Attendance

# def attendance_list(request):
#     attendance = Attendance.objects.select_related('employee').all()
#     return render(request, 'employees/attendance_list.html', {'attendance': attendance})
from django.shortcuts import render
from .models import Attendance, Employee
from django.contrib.auth.decorators import login_required


# def attendance_list(request):
#     q = request.GET.get('q', '')
#     attendance = Attendance.objects.all()

#     if q:
#         attendance = attendance.filter(employee__first_name__icontains=q)

#     employees = Employee.objects.all()  # ✅ Add this line

#     return render(request, 'employees/attendance_list.html', {
#         'attendance': attendance,
#         'employees': employees,  # ✅ Pass to template
#     })
@login_required
def attendance_list(request):
    attendance = Attendance.objects.select_related('employee').all().order_by('-date')
    employees = Employee.objects.all()
    q = request.GET.get("q", "")

    if q:
        attendance = attendance.filter(employee__first_name__icontains=q)

    return render(request, "employees/attendance_list.html", {
        "attendance": attendance,
        "employees": employees
    })

from django.contrib.auth.decorators import login_required



@login_required
def employee_attendance(request):
    attendance = Attendance.objects.filter(employee=request.user.employee).order_by('-date')

    return render(request, "employees/employee_attendance.html", {
        "attendance": attendance,
    })

# leave_list-----------------------------
# def leave_list(request):
#     leaves = Leave.objects.select_related('employee').all()
#     return render(request, 'employees/leave_list.html', {'leaves': leaves})
# views.py
# def leave_list(request):
#     if request.user.is_superuser:
#         # ADMIN → see all employees
#         leaves = Leave.objects.all()
#     else:
#         # EMPLOYEE → see only their own leaves
#         leaves = Leave.objects.filter(employee=request.user.employee)

#     return render(request, "leave_list.html", {
#         "leaves": leaves,
#         "employees": Employee.objects.all() if request.user.is_superuser else None
#     })
def employee_dashboard(request):
    employee = request.user.employee
    leaves = Leave.objects.filter(employee=employee).order_by('-date_from')

    return render(request, 'employees/employee_leave_list.html', {
        'employee': employee,
        'leaves': leaves
    })
def leave_list(request):
    leaves = Leave.objects.all().order_by('start_date')
    return render(request, 'employees/leave_list.html', {'leaves': leaves})
@login_required
def employee_leave_list(request):
    # Only show logged-in employee leaves
    if not hasattr(request.user, 'employee'):
        return redirect('dashboard')

    employee = request.user.employee
    leaves = Leave.objects.filter(employee=employee).order_by('-start_date')

    return render(request, "employees/employee_leave_list.html", {
        "leaves": leaves,
        "employee": employee
    })
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Employee, Leave
from django.contrib.auth.models import User





from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Attendance, Leave
from django.contrib import messages

def mark_attendance(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        date = request.POST.get('date')
        Attendance.objects.create(employee=employee, status=status, date=date)
        messages.success(request, f"Attendance marked for {employee.first_name}.")
        return redirect('employee_list')

def apply_leave(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')
        Leave.objects.create(employee=employee, start_date=start_date, end_date=end_date, reason=reason, status='Pending')
        messages.success(request, f"Leave applied for {employee.first_name}.")
        return redirect('employee_list')

# --------------------approval email ---------------


from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_admin)
def approve_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    leave.status = "Approved"
    leave.save()

    # Notify employee by email
    send_mail(
        subject="Leave Approved",
        message=f"Your leave from {leave.start_date} to {leave.end_date} has been approved.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[leave.employee.email],
        fail_silently=True
    )

    messages.success(request, f"Leave for {leave.employee.first_name} approved.")
    return redirect("leave_list")

@user_passes_test(is_admin)
def reject_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    leave.status = "Rejected"
    leave.save()

    # Notify employee by email
    send_mail(
        subject="Leave Rejected",
        message=f"Your leave from {leave.start_date} to {leave.end_date} has been rejected.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[leave.employee.email],
        fail_silently=True
    )

    messages.warning(request, f"Leave for {leave.employee.first_name} rejected.")
    return redirect("leave_list")

# --------------------------mark att-----------------
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employee, Attendance
from datetime import datetime

def mark_attendance_all(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        status = request.POST.get('status')
        date = request.POST.get('date')

        Attendance.objects.create(
            employee_id=employee_id,
            status=status,
            date=datetime.strptime(date, "%Y-%m-%d")
        )
        messages.success(request, "Attendance marked successfully!")
        return redirect('attendance_list')



def leave_list(request):
    leaves = Leave.objects.select_related('employee').all()
    employees = Employee.objects.all()  # 👈 add this line
    return render(request, 'employees/leave_list.html', {'leaves': leaves, 'employees': employees})

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employee, Leave

def apply_leave_all(request):
    if request.method == "POST":
        employee_id = request.POST.get("employee_id")
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        reason = request.POST.get("reason")

        employee = Employee.objects.get(id=employee_id)
        Leave.objects.create(
            employee=employee,
            start_date=from_date,
            end_date=to_date,
            reason=reason,
            status="Pending"
        )

        messages.success(request, "Leave applied successfully!")
        return redirect("employee_leave_list")

    employees = Employee.objects.all()
    leaves = Leave.objects.all()
    return render(request, "employees/employee_leave_list.html", {"employees": employees, "leaves": leaves})




from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

def apply_leave(request):
    if request.method == "POST":
        employee_id = request.POST.get("employee_id")
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        reason = request.POST.get("reason")

        employee = Employee.objects.get(id=employee_id)
        leave = Leave.objects.create(
            employee=employee,
            start_date=from_date,
            end_date=to_date,
            reason=reason,
            status="Pending"
        )

        # Send email to all admins
        admin_emails = User.objects.filter(is_staff=True).values_list('email', flat=True)
        send_mail(
            subject=f"Leave Request from {employee.first_name} {employee.last_name}",
            message=f"""
            Employee: {employee.first_name} {employee.last_name}
            From: {from_date}
            To: {to_date}
            Reason: {reason}
            Status: Pending
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=admin_emails,
            fail_silently=True
        )

        messages.success(request, "Leave applied successfully! Admins have been notified.")
        return redirect("leave_list")

    employees = Employee.objects.all()
    leaves = Leave.objects.all()
    return render(request, "employees/leave_list.html", {"employees": employees, "leaves": leaves})

        
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Payroll
from django.contrib import messages

def payroll_list(request):
    payrolls = Payroll.objects.all()
    employees = Employee.objects.all()
    return render(request, 'employees/payroll_list.html', {'payrolls': payrolls, 'employees': employees})

def add_payroll(request, emp_id):
    employee = get_object_or_404(Employee, id=emp_id)
    if request.method == 'POST':
        month = request.POST['month']
        basic = float(request.POST['basic_salary'])
        hra = float(request.POST['hra'])
        allowances = float(request.POST['allowances'])
        provident_fund = float(request.POST['provident_fund'])
        tax = float(request.POST['tax'])

        Payroll.objects.create(
            employee=employee,
            month=month,
            basic_salary=basic,
            hra=hra,
            allowances=allowances,
            provident_fund=provident_fund,
            tax=tax
        )
        messages.success(request, f"Payroll for {employee.first_name} generated.")
        return redirect('payroll_list')

    return render(request, 'employees/add_payroll.html', {'employee': employee})
def add_payroll_redirect(request):
    emp_id = request.GET.get('emp_id')
    if emp_id:
        return redirect('add_payroll', emp_id=emp_id)
    return redirect('payroll_list')


import csv
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Payroll

# CSV Export
def export_payroll_csv(request):
    payrolls = Payroll.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="payrolls.csv"'

    writer = csv.writer(response)
    writer.writerow(['Employee', 'Month', 'Basic Salary', 'HRA', 'Allowances', 'Provident Fund', 'Tax', 'Net Salary'])
    
    for p in payrolls:
        writer.writerow([
            f"{p.employee.first_name} {p.employee.last_name}",
            p.month,
            p.basic_salary,
            p.hra,
            p.allowances,
            p.provident_fund,
            p.tax,
            p.net_salary
        ])
    
    return response

# PDF Export
def export_payroll_pdf(request):
    payrolls = Payroll.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="payrolls.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, 800, "Payroll Records")

    p.setFont("Helvetica", 10)
    y = 760
    p.drawString(30, y, "Employee")
    p.drawString(150, y, "Month")
    p.drawString(210, y, "Basic")
    p.drawString(260, y, "HRA")
    p.drawString(300, y, "Allowances")
    p.drawString(370, y, "PF")
    p.drawString(410, y, "Tax")
    p.drawString(450, y, "Net Salary")
    y -= 20

    for record in payrolls:
        p.drawString(30, y, f"{record.employee.first_name} {record.employee.last_name}")
        p.drawString(150, y, record.month)
        p.drawString(210, y, str(record.basic_salary))
        p.drawString(260, y, str(record.hra))
        p.drawString(300, y, str(record.allowances))
        p.drawString(370, y, str(record.provident_fund))
        p.drawString(410, y, str(record.tax))
        p.drawString(450, y, str(record.net_salary))
        y -= 20
        if y < 50:
            p.showPage()
            y = 800

    p.save()
    return response
# emp detail---------------------------------


from django.shortcuts import render, get_object_or_404
from .models import Employee, Leave, Payroll

def employee_detail(request):
    query = request.GET.get('q', '')
    employee = None
    leaves = None
    payrolls = None

    if query:
        employee = Employee.objects.filter(first_name__icontains=query) | Employee.objects.filter(last_name__icontains=query)
        if employee.exists():
            employee = employee.first()  # take first match
            leaves = Leave.objects.filter(employee=employee).order_by('-start_date')
            payrolls = Payroll.objects.filter(employee=employee).order_by('-month')
        else:
            employee = None

    return render(request, 'employees/employee_detail.html', {
        'employee': employee,
        'leaves': leaves,
        'payrolls': payrolls,
        'query': query
    })

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

def register(request):
    if request.method == "POST":
        full_name = request.POST['full_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password1, email=email)
        user.first_name = full_name
        user.save()
        messages.success(request, "Registration successful! Please sign in.")
        return redirect('login')

    return render(request, 'employees/register.html')



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

from .models import Employee, Meeting


# ------------------------------
# Employee Dashboard
# ------------------------------
@login_required
def employee_dashboard(request):
    # Match employee based on email (safe method)
    employee = Employee.objects.filter(email=request.user.email).first()

    context = {
        'employee': employee,
        'present_today': 5,
        'absent_today': 1,
        'leave_today': 2,
    }
    return render(request, 'employees/employee_dashboard.html', context)


# ------------------------------
# Login View
# ------------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('dashboard')  # admin dashboard
            else:
                return redirect('employee_dashboard')  # employee dashboard
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'employees/login.html')


# ------------------------------
# Attendance Events API
# ------------------------------
def attendance_events(request):
    events = [
        {"title": "Present", "start": "2025-11-01", "color": "#28a745"},
        {"title": "Leave", "start": "2025-11-05", "color": "#dc3545"},
    ]
    return JsonResponse(events, safe=False)


# ------------------------------
# Meeting Section Page
# ------------------------------
def meeting_section(request):
    employees = Employee.objects.all()
    return render(request, 'employees/meeting_section.html', {'employees': employees})


# ------------------------------
# Schedule Meeting + Send Email
# ------------------------------

@login_required
def schedule_meeting(request):
    # Only superuser can schedule meeting
    if not request.user.is_superuser:
        return render(request, "employees/no_employee.html")

    if request.method == "POST":
        title = request.POST.get('title')
        datetime_value = request.POST.get('datetime')
        details = request.POST.get('details')
        employee_ids = request.POST.getlist('employees')

        meeting = Meeting.objects.create(
            title=title,
            datetime=datetime_value,
            details=details
        )
        meeting.employees.set(employee_ids)

        # Email all selected employees
        selected_employees = Employee.objects.filter(id__in=employee_ids)

        for emp in selected_employees:
            if emp.email:
                send_mail(
                    f"📅 New Meeting Scheduled: {title}",
                    f"""
Dear {emp.first_name},

A new meeting has been scheduled.

📌 Title: {title}
📅 Date & Time: {datetime_value}
📝 Details: {details}

Regards,
Admin
""",
                    "muppuraj11@gmail.com",
                    [emp.email],
                    fail_silently=True,
                )

        messages.success(request, "Meeting scheduled successfully!")
        return redirect('dashboard')

    employees = Employee.objects.all()
    return render(request, 'employees/meeting_section.html', {'employees': employees})



# ------------------------------
# Unified meetings view
# ------------------------------

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Employee, Meeting
from django.core.mail import send_mail
@login_required
def meetings_view(request):
    # ADMIN (superuser only)
    if request.user.is_superuser:
        meetings = Meeting.objects.all().order_by('-datetime')
        return render(request, 'employees/meetings.html', {
            'meetings': meetings,
            'is_admin': True
        })

    # EMPLOYEE
    if hasattr(request.user, "employee"):
        employee = request.user.employee
        meetings = employee.meetings.all().order_by('datetime')
        return render(request, 'employees/meetings.html', {
            'meetings': meetings,
            'is_admin': False
        })

    # No employee profile
    return render(request, "employees/no_employee.html")






# chat------------------------------
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import ChatMessage
from django.utils import timezone


def chat_with_employee(request, employee_id):
    employee = User.objects.get(id=employee_id)

    # Load messages between admin and employee
    messages = ChatMessage.objects.filter(
        sender__in=[request.user, employee],
        receiver__in=[request.user, employee]
    ).order_by("timestamp")

    return render(request, "employees/chatbox.html", {
        "employee": employee,
        "messages": messages
    })


def send_message(request):
    if request.method == "POST":
        message_text = request.POST.get("message", "").strip()
        receiver_id = request.POST.get("receiver_id")

        if not receiver_id or not receiver_id.isdigit():
            return JsonResponse({"status": "error", "message": "Invalid receiver"}, status=400)

        receiver = User.objects.get(id=int(receiver_id))

        ChatMessage.objects.create(
            sender=request.user,
            receiver=receiver,
            message=message_text,
            timestamp=timezone.now()
        )

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "invalid_method"}, status=405)


def admin_chat_list(request):
    if not request.user.is_superuser:
        return redirect("employee_dashboard")

    employees = User.objects.filter(is_superuser=False)

    return render(request, "employees/admin_chat_list.html", {
        "employees": employees
    })


def employee_dashboard(request):
    admin_user = User.objects.filter(is_superuser=True).first()

    return render(request, "employees/employee_dashboard.html", {
        "admin_id": admin_user.id
    })
def chatbox(request):
    return render(request, 'employees/chatbox.html')
# wfh------------------------


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from .models import WorkFromHome, Employee


# -------------------------
# LOGIN VIEW
# -------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('dashboard')        # Admin dashboard
            else:
                return redirect('employee_dashboard')

        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'employees/login.html')



# -------------------------
# EMPLOYEE DASHBOARD
# -------------------------
def employee_dashboard(request):

    if not hasattr(request.user, "employee"):
        return render(request, "employees/no_employee.html")

    employee = request.user.employee

    recent_wfh = WorkFromHome.objects.filter(
        employee=employee
    ).order_by('-date')[:5]

    return render(request, "employees/employee_dashboard.html", {
        "recent_wfh": recent_wfh,
    })



# -------------------------
# APPLY WFH
# -------------------------
def apply_wfh(request):

    if not hasattr(request.user, "employee"):
        return render(request, "employees/no_employee.html")

    employee = request.user.employee

    if request.method == 'POST':
        date = request.POST['date']
        reason = request.POST['reason']

        wfh = WorkFromHome.objects.create(
            employee=employee,
            date=date,
            reason=reason,
            applied_on=timezone.now()
        )

        # -------------------------
        # SEND EMAIL TO ADMIN
        # -------------------------
        send_mail(
            subject="New Work From Home Request",
            message=f"""
Employee: {employee.first_name} {employee.last_name}
Date: {date}
Reason: {reason}
            """,
            from_email="yourgmail@gmail.com",
            recipient_list=["muppuraj11@gmail.com"],
        )

        return redirect('wfh_list')

    return render(request, "employees/apply_wfh.html")



# -------------------------
# APPROVE / REJECT WFH
# -------------------------
def approve_wfh(request, wfh_id):
    wfh = WorkFromHome.objects.get(id=wfh_id)
    wfh.status = "Approved"
    wfh.save()

    send_mail(
        "WFH Approved",
        f"Your WFH request on {wfh.date} is approved.",
        "muppuraj11@gmail.com",
        [wfh.employee.email],
    )

    return redirect("wfh_list")


def reject_wfh(request, wfh_id):
    wfh = WorkFromHome.objects.get(id=wfh_id)
    wfh.status = "Rejected"
    wfh.save()

    send_mail(
        "WFH Request Rejected",
        f"Your WFH request on {wfh.date} is rejected.",
        "muppuraj11@gmail.com",
        [wfh.employee.email],
    )

    return redirect("wfh_list")



# -------------------------
# WFH LIST
# -------------------------
def wfh_list(request):

    if request.user.is_superuser:
        wfh = WorkFromHome.objects.all().order_by('-applied_on')

    else:
        if not hasattr(request.user, "employee"):
            return render(request, "employees/no_employee.html")

        wfh = WorkFromHome.objects.filter(
            employee=request.user.employee
        )

    return render(request, "employees/wfh_list.html", {"wfh": wfh})
# def wfh_list(request):
#     if request.user.is_superuser:
#         wfh = WorkFromHome.objects.all().order_by('-applied_on')
#     else:
#         if not hasattr(request.user, "employee"):
#             return render(request, "employees/no_employee.html")

#         wfh = WorkFromHome.objects.filter(
#             employee=request.user.employee
#         )

#     return render(request, "employees/wfh_list.html", {"wfh": wfh})


# calender in-on-----------------------------
# views.py
from django.http import JsonResponse
from .models import EmployeeLoginLogout, Leave, WorkFromHome
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import EmployeeLoginLogout, Leave, WorkFromHome, Employee

@login_required
def attendance_events(request):
    user = request.user
    try:
        employee = Employee.objects.get(user=user)
    except Employee.DoesNotExist:
        return JsonResponse([], safe=False)  # No employee found

    events = []

    # Login/Logout as work range
    attendance = EmployeeLoginLogout.objects.filter(employee=employee)
    for a in attendance:
        if a.login_time and a.logout_time:
            events.append({
                "title": "Work",
                "start": a.login_time.isoformat(),
                "end": a.logout_time.isoformat(),
                "color": "#28a745"
            })
        else:
            if a.login_time:
                events.append({
                    "title": "Login",
                    "start": a.login_time.isoformat(),
                    "color": "#28a745"
                })
            if a.logout_time:
                events.append({
                    "title": "Logout",
                    "start": a.logout_time.isoformat(),
                    "color": "#dc3545"
                })

    # Leave
    leaves = Leave.objects.filter(employee=employee)
    for leave in leaves:
        if leave.start_date and leave.end_date:
            events.append({
                "title": "Leave",
                "start": leave.start_date.isoformat(),
                "end": leave.end_date.isoformat(),
                "color": "#ff0000"
            })

    # WFH
    wfh_events = WorkFromHome.objects.filter(employee=employee)
    for w in wfh_events:
        if w.date:
            events.append({
                "title": "WFH",
                "start": w.date.isoformat(),
                "color": "#f7c600"
            })

    print("Events:", events)  # debug
    return JsonResponse(events, safe=False)

from django.shortcuts import render
from .models import EmployeeLoginLogout

def login_logout_report(request):
    records = EmployeeLoginLogout.objects.select_related('employee').order_by('-login_time')
    return render(request, 'employees/login_logout_report.html', {'records': records})

# my profile--------------------
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# @login_required
# def my_profile(request):
#     employee = request.user.employee  # Get logged-in employee ONLY
#     return render(request, 'employees/my_profile.html', {'employee': employee})
@login_required
def my_profile(request):
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        employee = None

    return render(request, "employees/my_profile.html", {
        "employee": employee,
        "user": request.user
    })
