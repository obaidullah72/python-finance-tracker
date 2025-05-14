from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Bill
from .forms import BillForm
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings

@login_required
def dashboard(request):
    today = datetime.today().date()
    upcoming_bills = Bill.objects.filter(user=request.user, due_date__gte=today, is_paid=False).order_by('due_date')
    overdue_bills = Bill.objects.filter(user=request.user, due_date__lt=today, is_paid=False).order_by('due_date')
    return render(request, 'bills/dashboard.html', {'upcoming_bills': upcoming_bills, 'overdue_bills': overdue_bills})

@login_required
def add_bill(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.user = request.user
            bill.save()
            # Send email notification (optional)
            send_mail(
                'New Bill Added',
                f'You have added a new bill: {bill.name} due on {bill.due_date}.',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=True,
            )
            return redirect('dashboard')
    else:
        form = BillForm()
    return render(request, 'bills/add_bills.html', {'form': form})

@login_required
def mark_paid(request, bill_id):
    bill = Bill.objects.get(id=bill_id, user=request.user)
    bill.is_paid = True
    bill.save()
    return redirect('dashboard')