from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.DashboardView.as_view(), name='tracker-dashboard'),
    path('add/', views.AddTransactionView.as_view(), name='add_transaction'),
    path('edit/<int:pk>/', views.EditTransactionView.as_view(), name='edit_transaction'),
    path('delete/<int:pk>/', views.DeleteTransactionView.as_view(), name='delete_transaction'),
    path('transactions/', views.TransactionListView.as_view(), name='transaction_list'),
    path('report/', views.ReportView.as_view(), name='report'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category_add'),
    path('categories/edit/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='category_delete'),
]