from django.urls import path
from .views import UserProfileUpdateView, PasswordUpdateView

urlpatterns = [
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('password/update/', PasswordUpdateView.as_view(), name='password-update'),
]