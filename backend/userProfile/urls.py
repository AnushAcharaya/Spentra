from django.urls import path
from .views import UserProfileView, AdminUserProfileView

urlpatterns = [
    # User profile endpoints
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    
    # Admin endpoints
    path('admin/profiles/', AdminUserProfileView.as_view(), name='admin-profiles'),
    path('admin/profiles/<int:user_id>/', AdminUserProfileView.as_view(), name='admin-profile-detail'),
]