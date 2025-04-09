from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User  # Import User model
from django.http import HttpResponseBadRequest
from django.contrib.auth.forms import UserChangeForm  # Import UserChangeForm
from django.urls import reverse_lazy
from django.db.models import Sum, Q
from django.http import HttpResponse
from django.utils import timezone
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import csv, json
from decimal import Decimal
from django.shortcuts import render
from .models import Transaction, Category
from .forms import TransactionForm, RegisterForm, LoginForm, CustomUserChangeForm, CategoryForm



class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'tracker/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('tracker-dashboard')
        return render(request, 'tracker/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'tracker/login.html'
    authentication_form = LoginForm


class CustomLogoutView(LogoutView):
    next_page = 'login'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'tracker/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.now()
        transactions = Transaction.objects.filter(user=user)

        selected_month = self.request.GET.get('month')
        if selected_month:
            try:
                year, month = map(int, selected_month.split('-'))
                transactions = transactions.filter(date__year=year, date__month=month)
            except ValueError:
                pass

        total_income = transactions.filter(Q(category__is_income=True) | Q(category__isnull=True)).aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = transactions.filter(category__is_income=False).aggregate(Sum('amount'))['amount__sum'] or 0
        balance = total_income - total_expenses

        category_data = transactions.filter(category__is_income=False).values('category__name').annotate(total=Sum('amount'))
        category_labels = [item['category__name'] for item in category_data]
        category_values = [float(item['total']) for item in category_data] if category_data else [0]

        all_transactions = Transaction.objects.filter(user=user).order_by('date')
        savings_data = {}
        running_balance = Decimal('0')
        for t in all_transactions:
            if t.category is None:
                running_balance += t.amount
            else:
                running_balance += t.amount if t.category.is_income else -t.amount
            savings_data[str(t.date)] = float(running_balance)

        context.update({
            'total_income': total_income,
            'total_expenses': total_expenses,
            'balance': balance,
            'category_labels': json.dumps(category_labels),
            'category_values': json.dumps(category_values),
            'savings_labels': json.dumps(list(savings_data.keys()) or ['No Data']),
            'savings_values': json.dumps(list(savings_data.values()) or [0]),
            'has_transactions': transactions.exists(),
            'selected_month': selected_month or today.strftime('%Y-%m'),
        })
        return context


class AddTransactionView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'tracker/add_transaction.html'
    success_url = reverse_lazy('tracker-dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        transaction = form.save(commit=False)
        transaction.user = self.request.user
        transaction_type = form.cleaned_data['transaction_type']
        category = form.cleaned_data['category']

        if transaction_type == 'expense' and category:
            if not category.is_income:
                transaction.category = category
            else:
                form.add_error('category', "Please select an expense category.")
                return self.form_invalid(form)
        elif transaction_type == 'income' and category:
            if category.is_income:
                transaction.category = category
            else:
                form.add_error('category', "Please select an income category.")
                return self.form_invalid(form)
        transaction.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Default to no transaction type on GET request
        transaction_type = self.request.POST.get('transaction_type') if self.request.method == 'POST' else None
        if transaction_type:
            categories = Category.objects.filter(user=self.request.user, is_income=(transaction_type == 'income'))
        else:
            categories = Category.objects.none()  # No categories until type is selected
        context['categories'] = categories
        context['transaction_type'] = transaction_type
        return context
    

class EditTransactionView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'tracker/edit_transaction.html'
    success_url = reverse_lazy('transaction_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class DeleteTransactionView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'tracker/transaction_list.html'
    success_url = reverse_lazy('transaction_list')


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'tracker/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        qs = Transaction.objects.filter(user=self.request.user)
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        category_id = self.request.GET.get('category')
        min_amount = self.request.GET.get('min_amount')
        max_amount = self.request.GET.get('max_amount')

        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)
        if category_id:
            qs = qs.filter(category_id=category_id)
        if min_amount:
            qs = qs.filter(amount__gte=min_amount)
        if max_amount:
            qs = qs.filter(amount__lte=max_amount)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(user=self.request.user)
        return context


class ReportView(LoginRequiredMixin, View):
    def get(self, request):
        today = timezone.now()
        transactions = Transaction.objects.filter(user=request.user)
        selected_month = request.GET.get('month')
        
        if selected_month:
            try:
                year, month = map(int, selected_month.split('-'))
                transactions = transactions.filter(date__year=year, date__month=month)
            except ValueError:
                pass

        export_type = request.GET.get('type')
        filename = selected_month or today.strftime('%Y-%m')

        if export_type == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="report_{filename}.csv"'
            writer = csv.writer(response)
            writer.writerow(['Date', 'Category', 'Amount', 'Description', 'Type'])
            
            for t in transactions:
                writer.writerow([
                    t.date.strftime('%Y-%m-%d'),
                    t.category.name if t.category else 'N/A',
                    f"{float(t.amount):.2f}",
                    t.description,
                    'Income' if t.category and t.category.is_income else 'Expense'
                ])
            return response

        elif export_type == 'pdf':
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="report_{filename}.pdf"'
            doc = SimpleDocTemplate(response, pagesize=letter)
            
            data = [['Date', 'Category', 'Amount', 'Description', 'Type']]
            for t in transactions:
                data.append([
                    t.date.strftime('%Y-%m-%d'),
                    t.category.name if t.category else 'N/A',
                    f"{float(t.amount):.2f}",
                    t.description,
                    'Income' if t.category and t.category.is_income else 'Expense'
                ])
            
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), '#d3d3d3'),
                ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, '#000000'),
            ]))
            doc.build([table])
            return response

        return render(request, 'tracker/report.html', {
            'selected_month': filename,
        })


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'tracker/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm  # Use the custom form
    template_name = 'tracker/edit_profile.html'  # Ensure this matches your template path
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        print(f"POST data: {request.POST}")
        if request.POST.get('_method') == 'PUT':
            return super().post(request, *args, **kwargs)  # Handle as update
        print.error("Invalid method: _method not set to PUT")
        return HttpResponseBadRequest("Invalid method")

    def form_valid(self, form):
        print("Form is valid, saving changes")
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print.error(f"Form is invalid: {form.errors}")
        return super().form_invalid(form)
    
    
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'tracker/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

# Category Create View (Dedicated Page)
class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'tracker/add_category.html'  # New template
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# Category Update View (Dedicated Page)
class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'tracker/edit_category.html'  # New template
    success_url = reverse_lazy('category_list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

# Category Delete View
class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'tracker/delete_category.html'  # New template for confirmation
    success_url = reverse_lazy('category_list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    
    
