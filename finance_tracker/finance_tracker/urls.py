from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import CustomLoginView, CustomLogoutView, home, RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'), 
    path('tracker/', include('tracker.urls'), name='tracker'),
    path('budget/', include('budget.urls'), name='budget'), 
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)