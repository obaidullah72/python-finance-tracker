from django.urls import path
from . import views

urlpatterns = [
    path('', views.budget_dashboard, name='budget_dashboard'),
    path('add/', views.add_budget, name='add_budget'),
]