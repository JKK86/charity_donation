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

from users.forms import UserLoginForm, UserPasswordResetForm, SetNewPassword

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),

    path('login/', auth_views.LoginView.as_view(authentication_form=UserLoginForm), name='login'),
    path('logout/', auth_views.logout_then_login, name='logout'),
    path('register/', users_views.UserRegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>', users_views.ActivateView.as_view(), name='account_activation_confirm'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=UserPasswordResetForm),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(form_class=SetNewPassword),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('', views.LandingPageView.as_view(), name='start'),
    path('add_donation/', views.AddDonationView.as_view(), name='add_donation'),
    path('user_profile/', users_views.UserProfile.as_view(), name='user_profile'),
    path('edit_profile/', users_views.EditProfile.as_view(), name='edit_profile'),
    path('contact/', views.ContactView.as_view(), name='contact')

]
