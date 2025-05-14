from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='bill_dashboard'),
    path('add/', views.add_bill, name='add_bill'),
    path('mark_paid/<int:bill_id>/', views.mark_paid, name='mark_paid'),
]