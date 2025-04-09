from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Budget, Transaction
from django.db.models import Sum
from datetime import datetime

@login_required
def budget_dashboard(request):
    categories = Category.objects.filter(user=request.user)
    budgets = Budget.objects.filter(user=request.user, start_date__month=datetime.now().month)
    transactions = Transaction.objects.filter(user=request.user, date__month=datetime.now().month)

    # Calculate spending per category
    spending = transactions.values('category__name').annotate(total=Sum('amount'))
    budget_data = []
    for budget in budgets:
        spent = next((s['total'] for s in spending if s['category__name'] == budget.category.name), 0)
        budget_data.append({
            'category': budget.category.name,
            'budgeted': float(budget.amount),
            'spent': float(spent),
            'remaining': float(budget.amount) - float(spent),
            'over_budget': spent > budget.amount
        })

    context = {
        'budget_data': budget_data,
        'categories': categories,
    }
    return render(request, 'budget/dashboard.html', context)

@login_required
def add_budget(request):
    if request.method == 'POST':
        category_id = request.POST['category']
        amount = request.POST['amount']
        period = request.POST['period']
        start_date = request.POST['start_date']
        
        Budget.objects.create(
            user=request.user,
            category=Category.objects.get(id=category_id, user=request.user),
            amount=amount,
            period=period,
            start_date=start_date
        )
        return redirect('budget_dashboard')
    
    categories = Category.objects.filter(user=request.user)
    return render(request, 'budget/add_budget.html', {'categories': categories})