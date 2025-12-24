from django.core.management.base import BaseCommand
from django.utils import timezone
from calendar import monthrange

from gate.models import Employee, Attendance, SalaryPayment


class Command(BaseCommand):
    help = 'Process payroll for a given month and year (simulate bank credit)'

    def add_arguments(self, parser):
        parser.add_argument('--month', type=int, help='Month number (1-12). Defaults to current month')
        parser.add_argument('--year', type=int, help='Year. Defaults to current year')
        parser.add_argument('--pay', action='store_true', help='Mark payments as paid (simulate bank credit)')

    def handle(self, *args, **options):
        now = timezone.now()
        month = options.get('month') or now.month
        year = options.get('year') or now.year
        pay_flag = options.get('pay')

        days_in_month = monthrange(year, month)[1]
        working_days = 0
        for d in range(1, days_in_month + 1):
            weekday = timezone.datetime(year, month, d).weekday()
            if weekday < 5:
                working_days += 1

        self.stdout.write(f'Processing payroll for {month}/{year} (working days: {working_days})')

        for emp in Employee.objects.all():
            present_count = Attendance.objects.filter(employee=emp, date__year=year, date__month=month, present=True).count()
            amount = 0
            if working_days > 0:
                amount = (emp.basic_salary / working_days) * present_count

            payment, created = SalaryPayment.objects.get_or_create(
                employee=emp, month=month, year=year,
                defaults={'days_present': present_count, 'amount': amount}
            )
            if not created:
                payment.days_present = present_count
                payment.amount = amount
                payment.save()

            if pay_flag:
                payment.paid = True
                payment.paid_at = timezone.now()
                payment.save()
                self.stdout.write(f'Paid {payment.amount} to {emp.emp_id} ({emp.name})')
            else:
                self.stdout.write(f'Computed {payment.amount} for {emp.emp_id} ({emp.name})')

        self.stdout.write(self.style.SUCCESS('Payroll processing complete.'))
