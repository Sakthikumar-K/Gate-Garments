"""
URL configuration for garments project.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('employees/', views.employees_list, name='employees'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('payroll/process/', views.process_payroll, name='process_payroll'),
]