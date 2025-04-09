from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tracker_categories')
    # Added related_name to distinguish from budget.Category.user
    is_income = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tracker_transactions')
    # Added related_name to distinguish from budget.Transaction.user
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(null=True, blank=True)  # Optional
    description = models.TextField(blank=True, null=True)  # Optional
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name if self.category else 'No Category'} - {self.amount} on {self.date or 'No Date'}"