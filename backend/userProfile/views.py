from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.conf import settings
from .serializers import UserProfileSerializer, UserSerializer
from .models import UserProfile
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

class UserProfileView(APIView):
    """
    API view for retrieving and updating the authenticated user's profile
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    
    def get_permissions(self):
        """
        Allow unauthenticated access in DEBUG mode for GET requests only
        """
        if self.request.method == 'GET' and getattr(settings, 'DEBUG', False):
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        """
        Retrieve the user's profile information
        """
        # Check if user is authenticated
        if not request.user.is_authenticated:
            # Return demo data for unauthenticated users in DEBUG mode
            if getattr(settings, 'DEBUG', False):
                demo_data = {
                    'id': 0,
                    'full_name': 'Demo User',
                    'photo': None,
                    'photo_url': None,
                    'first_name': 'Demo',
                    'last_name': 'User',
                    'gender': 'other',
                    'country': 'Sample Country',
                    'language': 'English',
                    'location': 'Sample Location',
                    'bio': 'This is a demo profile for testing purposes.',
                    'date_updated': '2025-04-30T12:00:00Z'
                }
                return Response(demo_data)
            else:
                return Response(
                    {"detail": "Authentication credentials were not provided."},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        
        # For authenticated users, return their profile
        try:
            # Ensure profile exists
            profile, created = UserProfile.objects.get_or_create(
                user=request.user,
                defaults={
                    'full_name': request.user.username,
                    'email': request.user.email
                }
            )
            
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving profile for user {request.user.username}: {str(e)}")
            return Response(
                {"error": f"Error retrieving profile: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request):
        """
        Update the user's profile information
        """
        # Only allow updates if authenticated
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required for updating profiles."},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        try:
            # Ensure profile exists
            profile, created = UserProfile.objects.get_or_create(
                user=request.user,
                defaults={
                    'full_name': request.user.username,
                    'email': request.user.email
                }
            )
            
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Profile updated for user {request.user.username}")
                return Response(serializer.data)
            else:
                logger.warning(f"Invalid data for profile update: {serializer.errors}")
                return Response(
                    {
                        "status": "error",
                        "message": "Invalid data provided",
                        "errors": serializer.errors
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"Error updating profile for user {request.user.username}: {str(e)}")
            return Response(
                {"error": f"Error updating profile: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AdminUserProfileView(APIView):
    """
    Admin-only API to manage all user profiles
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request, user_id=None):
        """
        Retrieve user profile(s)
        """
        try:
            if user_id:
                # Get specific user
                user = User.objects.get(id=user_id)
                # Ensure profile exists
                profile, created = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={'full_name': user.username}
                )
                serializer = UserSerializer(user)
                return Response(serializer.data)
            else:
                # List all users with profiles
                users = User.objects.all()
                serializer = UserSerializer(users, many=True)
                return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Admin error retrieving profile(s): {str(e)}")
            return Response(
                {"error": f"Error retrieving profile(s): {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )