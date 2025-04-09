from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Transaction, Category

class TransactionForm(forms.ModelForm):
    transaction_type = forms.ChoiceField(
        choices=[('income', 'Income'), ('expense', 'Expense')],
        widget=forms.RadioSelect,
        label="Transaction Type"
    )

    class Meta:
        model = Transaction
        fields = ['transaction_type', 'category', 'amount', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)
        self.fields['category'].required = False  # Not required
        self.fields['date'].required = False  # Not required
        self.fields['description'].required = False  # Not required

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
 
 
class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  
        
        
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'is_income']
        widgets = {
            'is_income': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }