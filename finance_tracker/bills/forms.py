from django import forms
from .models import Bill

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['name', 'amount', 'due_date', 'frequency']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }