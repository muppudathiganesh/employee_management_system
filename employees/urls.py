from django.urls import path
from . import views

urlpatterns = [
    path('employees/', views.employee_list, name='employee_list'),
     path('payroll/', views.payroll_list, name='payroll_list'),
    path('payroll/add/<int:emp_id>/', views.add_payroll, name='add_payroll'),
    path('payroll/add/', views.add_payroll_redirect, name='add_payroll_redirect'),
  path('payroll/export/csv/', views.export_payroll_csv, name='export_payroll_csv'),
    path('payroll/export/pdf/', views.export_payroll_pdf, name='export_payroll_pdf'),
    

    # Add correct employee paths
    path('employee/add/', views.add_employee, name='add_employee'),
    path('employee/edit/<int:pk>/', views.edit_employee, name='edit_employee'),
    path('employee/delete/<int:pk>/', views.delete_employee, name='delete_employee'),

    # Login page
    path('', views.login_view, name='login'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('departments/', views.view_departments, name='view_departments'),
    path('departments/add/', views.add_department, name='add_department'),

   path('attendance/<int:employee_id>/', views.mark_attendance, name='mark_attendance'),
  
   # ✅ Add these new routes ↓↓↓
    path('leave/<int:leave_id>/approve/', views.approve_leave, name='approve_leave'),
    path('leave/<int:leave_id>/reject/', views.reject_leave, name='reject_leave'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('leave/', views.leave_list, name='leave_list'),
    path('attendance/mark_all/', views.mark_attendance_all, name='mark_attendance_all'),
  # urls.py
path('leave/apply/', views.apply_leave, name='apply_leave'),
# urls.py
path('leave/apply/<int:employee_id>/', views.apply_leave, name='apply_leave'),

    path('leave/all/', views.leave_list, name='leave_list'),
  path('employee/detail/', views.employee_detail, name='employee_detail'),
 path('logout/', views.logout_view, name='logout'),
path('register/', views.register, name='register'),
path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),

  
  
    

]
