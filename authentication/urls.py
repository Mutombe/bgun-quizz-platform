from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Other URL patterns
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'), 
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'), 

]