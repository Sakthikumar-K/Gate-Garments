from django.contrib import admin
from .models import Employee, Attendance, SalaryPayment


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('emp_id', 'name', 'basic_salary', 'bank_account')
	search_fields = ('emp_id', 'name')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
	list_display = ('employee', 'date', 'present', 'intime', 'outtime')
	list_filter = ('present', 'date')
	search_fields = ('employee__emp_id', 'employee__name')


@admin.register(SalaryPayment)
class SalaryPaymentAdmin(admin.ModelAdmin):
	list_display = ('employee', 'month', 'year', 'amount', 'paid')
	list_filter = ('paid', 'year', 'month')
	search_fields = ('employee__emp_id', 'employee__name')
