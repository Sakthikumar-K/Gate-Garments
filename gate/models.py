from django.db import models
from django.utils import timezone


# Employee working at the garment/shirt-stitching company
class Employee(models.Model):
    emp_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=(('M','Male'),('F','Female'),('O','Other')))
    address = models.CharField(max_length=255, blank=True)
    bank_account = models.CharField(max_length=64, blank=True)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.emp_id} - {self.name}"


# Daily attendance record for an employee
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=timezone.now)
    intime = models.TimeField(null=True, blank=True)
    outtime = models.TimeField(null=True, blank=True)
    present = models.BooleanField(default=True)

    class Meta:
        unique_together = (('employee', 'date'),)

    def __str__(self):
        return f"{self.employee.emp_id} - {self.date} - {'P' if self.present else 'A'}"


# Salary payment record (one row per employee per month)
class SalaryPayment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payments')
    month = models.PositiveSmallIntegerField()  # 1-12
    year = models.PositiveSmallIntegerField()
    days_present = models.PositiveSmallIntegerField(default=0)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = (('employee', 'month', 'year'),)

    def __str__(self):
        return f"{self.employee.emp_id} - {self.month}/{self.year} - {self.amount}"
    