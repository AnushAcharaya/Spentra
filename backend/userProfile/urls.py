from django.urls import path
from drf_yasg.utils import swagger_auto_schema
from .views import UserProfileView, AdminUserProfileView

# Apply swagger_auto_schema to views
UserProfileView = swagger_auto_schema(
    operation_description="User profile management endpoints",
    operation_summary="User Profile API"
)(UserProfileView)

AdminUserProfileView = swagger_auto_schema(
    operation_description="Admin-only user profile management endpoints",
    operation_summary="Admin User Profile API"
)(AdminUserProfileView)

urlpatterns = [
    # User profile endpoints
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    
    # Admin endpoints
    path('admin/profiles/', AdminUserProfileView.as_view(), name='admin-profiles'),
    path('admin/profiles/<int:user_id>/', AdminUserProfileView.as_view(), name='admin-profile-detail'),
]