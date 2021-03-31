"""charity_donation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from donation import views
from users import views as users_views
from django.contrib.auth import views as auth_views

from users.forms import UserLoginForm

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.LandingPageView.as_view(), name='start'),
    path('login/', auth_views.LoginView.as_view(authentication_form=UserLoginForm), name='login'),
    path('logout/', auth_views.logout_then_login, name='logout'),
    path('register/', users_views.UserRegisterView.as_view(), name='register'),
    path('add_donation/', views.AddDonationView.as_view(), name='add_donation'),
    path('user_profile/', users_views.UserProfile.as_view(), name='user_profile'),

]
