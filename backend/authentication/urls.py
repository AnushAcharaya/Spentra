print("authentication/urls.py loaded")

from django.urls import path
from drf_yasg.utils import swagger_auto_schema
from .views import RegisterView, LoginView, PasswordResetView, OTPVerifyView, ProtectedView, RequestPasswordResetView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Apply swagger_auto_schema to views
RegisterView = swagger_auto_schema(
    operation_description="User registration endpoints",
    operation_summary="Registration API"
)(RegisterView)

LoginView = swagger_auto_schema(
    operation_description="User authentication endpoints",
    operation_summary="Authentication API"
)(LoginView)

PasswordResetView = swagger_auto_schema(
    operation_description="Password reset endpoints",
    operation_summary="Password Reset API"
)(PasswordResetView)

OTPVerifyView = swagger_auto_schema(
    operation_description="OTP verification endpoints",
    operation_summary="OTP Verification API"
)(OTPVerifyView)

ProtectedView = swagger_auto_schema(
    operation_description="Protected endpoints requiring authentication",
    operation_summary="Protected API"
)(ProtectedView)

RequestPasswordResetView = swagger_auto_schema(
    operation_description="Password reset request endpoints",
    operation_summary="Password Reset Request API"
)(RequestPasswordResetView)

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