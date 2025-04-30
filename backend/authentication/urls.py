print("authentication/urls.py loaded")

from django.urls import path
from .views import RegisterView, LoginView, PasswordResetView, OTPVerifyView, ProtectedView, RequestPasswordResetView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('request-password-reset/', RequestPasswordResetView.as_view(), name='request_password_reset'),
    path('otp-verify/', OTPVerifyView.as_view(), name='otp_verify'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('auth/password-reset/', PasswordResetView.as_view(), name='auth_password_reset'),  # Adding the endpoint mentioned in the error
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('protected/', ProtectedView.as_view(), name='protected'),
]