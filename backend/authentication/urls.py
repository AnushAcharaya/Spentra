print("authentication/urls.py loaded")

from django.urls import path
from .views import RegisterView, LoginView, PasswordResetView, OTPVerifyView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('otp-verify/', OTPVerifyView.as_view(), name='otp_verify'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
]