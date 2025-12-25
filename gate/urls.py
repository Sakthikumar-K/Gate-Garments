"""
URL configuration for garments project.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('employees/', views.employees_list, name='employees_list'),
    path('add-employee/', views.add_employee, name='add_employees'),
    path('edit-employee/<int:id>/', views.edit_employee, name='edit_employees'),
    path('delete-employee/<int:id>/', views.delete_employee, name='delete_employee'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('process-payroll/', views.process_payroll, name='process_payroll'),
]
