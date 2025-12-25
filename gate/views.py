from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from calendar import monthrange

from .models import Employee, Attendance, SalaryPayment


def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Simple check for demo
        if username == 'admin' and password == 'admin':
            request.session['logged_in'] = True
            return redirect('employees.html')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'Login.html')


def add_employee(request):
    if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        name = request.POST.get('name')
        address = request.POST.get('address')
        age = request.POST.get('age')
        bank_account = request.POST.get('bank_account')
        salary = request.POST.get('salary')
        Employee.objects.create(
            emp_id=emp_id,
            name=name,
            age=age,
            address=address,
            bank_account=bank_account,
            basic_salary=salary
        )
        messages.success(request, 'Employee added successfully')
        return redirect('employees.html')
    return render(request, 'add_employees.html')


def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.name = request.POST.get('name')
        employee.basic_salary = request.POST.get('salary')
        employee.save()
        messages.success(request, 'Employee updated successfully')
        return redirect('employees.html')
    return render(request, 'edit_employees.html', {'employee': employee})


def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    messages.success(request, 'Employee deleted successfully')
    return redirect('employees.html')


def employees_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees.html', {'employees': employees})


def mark_attendance(request):
    if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        date_str = request.POST.get('date')
        employee = get_object_or_404(Employee, emp_id=emp_id)
        if date_str:
            date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            date = timezone.now().date()
        attendance, created = Attendance.objects.get_or_create(employee=employee, date=date,
                                                               defaults={'present': True})
        if not created:
            attendance.present = True
            attendance.save()
        messages.success(request, f'Attendance marked for {employee.name} on {date}')
        return redirect('employees.html')
    return render(request, 'add_employees.html')


def process_payroll(request):
    # Simple payroll processor: compute days present and pro-rate salary
    if request.method == 'POST':
        month = int(request.POST.get('month'))
        year = int(request.POST.get('year'))
        # compute working days in month (weekdays)
        days_in_month = monthrange(year, month)[1]
        working_days = 0
        for d in range(1, days_in_month + 1):
            weekday = timezone.datetime(year, month, d).weekday()
            if weekday < 5:
                working_days += 1

        processed = []
        for emp in Employee.objects.all():
            present_count = Attendance.objects.filter(employee=emp, date__year=year, date__month=month, present=True).count()
            if working_days == 0:
                amount = 0
            else:
                amount = (emp.basic_salary / working_days) * present_count
            payment, created = SalaryPayment.objects.get_or_create(employee=emp, month=month, year=year,
                                                                   defaults={'days_present': present_count, 'amount': amount})
            if not created:
                payment.days_present = present_count
                payment.amount = amount
                payment.save()
            processed.append({'emp': emp.emp_id, 'name': emp.name, 'amount': float(amount), 'days_present': present_count})

def pay_salary(request):
    if request.method == 'POST':
        month = int(request.POST.get('month'))
        year = int(request.POST.get('year'))
        for payment in SalaryPayment.objects.filter(month=month, year=year, paid=False):
            payment.paid = True
            payment.paid_at = timezone.now()
            payment.save()
            # Simulate bank credit
            messages.success(request, f'Salary credited to {payment.employee.name} account {payment.employee.bank_account}: {payment.amount}')
        return redirect('employees.html')
    return redirect('employees.html')