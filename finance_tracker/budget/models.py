from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budget_categories')
    # Added related_name to distinguish from tracker.Category.user

    def __str__(self):
        return self.name

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.CharField(max_length=10, choices=[('monthly', 'Monthly'), ('weekly', 'Weekly')])
    start_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name} - {self.period} Budget"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budget_transactions')
    # Added related_name to distinguish from tracker.Transaction.user
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"