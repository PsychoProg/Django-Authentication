from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login', views.UserLogin.as_view(), name='login_url'),
    path('register', views.RegisterView.as_view(), name='register_url'),
    path('check-otp', views.CheckOtpView.as_view(), name='check_otp_url'),
]
