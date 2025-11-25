from django.urls import path
from . import views
from .views import chat_with_employee, send_message,employee_attendance,employee_detail



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
# path('leave/apply/<int:employee_id>/', views.apply_leave, name='apply_leave'),

path('leave/all/', views.leave_list, name='leave_list'),
path('employee/detail/', views.employee_detail, name='employee_detail'),




path('logout/', views.logout_view, name='logout'),
path('register/', views.register, name='register'),
path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
# ----meeting
  path('meeting_section/', views.meeting_section, name='meeting_section'),
  path('schedule_meeting/', views.schedule_meeting, name='schedule_meeting'),
# path('employee_meetings/', views.employee_meetings, name='employee_meetings'),
# path('admin_meetings/', views.admin_meetings, name='admin_meetings'),
 path('meetings/', views.meetings_view, name='meetings_view'),
#  chat---------------

path('chat/<int:employee_id>/', views.chat_with_employee, name='chat_with_employee'),
path('send-message/', views.send_message, name='send_message'),
path('chatbox/', views.chatbox, name='chatbox'),
path('chat/admin/', views.admin_chat_list, name='admin_chat_list'),
# wfh--------------------------
path("work-from-home/", views.wfh_list, name="wfh_list"),
path("apply-wfh/", views.apply_wfh, name="apply_wfh"),
path("approve-wfh/<int:wfh_id>/", views.approve_wfh, name="approve_wfh"),
path("reject-wfh/<int:wfh_id>/", views.reject_wfh, name="reject_wfh"),
# in_on---------------------------------
path("attendance-events/", views.attendance_events, name="attendance_events"),
path('login-logout-report/', views.login_logout_report, name='login_logout_report'),

path("my-attendance/", employee_attendance, name="employee_attendance"),
path('my-profile/', views.my_profile, name='my_profile'),
path("my-leaves/", views.employee_leave_list, name="employee_leave_list"),
path('employee/leaves/', views.employee_leave_list, name='employee_leave_list'),

   # Password reset flow
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
# emp_login
    path('employee/login/', views.employee_login, name='employee_login'),


# report daily------------

path("report/submit/", views.submit_daily_report, name="submit_daily_report"),
path("reports/daily/", views.admin_daily_reports, name="admin_daily_reports"),
path("report/edit/<int:report_id>/", views.edit_daily_report, name="edit_daily_report"),
path("report/delete/<int:report_id>/", views.delete_daily_report, name="delete_daily_report"),
path("admin/report/reply/<int:report_id>/", views.admin_reply_report, name="admin_reply_report"),
path("report/history/", views.employee_report_history, name="employee_report_history"),


# Ticket system
path("ticket/raise/", views.raise_ticket, name="raise_ticket"),
path("tickets/admin/", views.admin_view_tickets, name="admin_view_tickets"),
path("ticket/reply/<int:ticket_id>/", views.admin_reply_ticket, name="admin_reply_ticket"),
path("tickets/history/", views.employee_ticket_history, name="employee_ticket_history"),

    path('punch-in/', views.punch_in, name='punch_in'),
    path('punch-out/', views.punch_out, name='punch_out'),
    path('admin-punch-records/', views.punch_in_out_admin, name='punch_in_out_admin'),
 # ---------------- Search ----------------
    path('search/', views.employee_details_search, name='employee_search'),


   

]
