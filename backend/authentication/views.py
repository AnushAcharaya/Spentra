from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer, PasswordResetSerializer
from .serializers import OTPVerifySerializer, RequestPasswordResetSerializer
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Send confirmation email
            try:
                send_mail(
                    subject='Welcome to Our Platform',
                    message='Thank you for registering!',
                    from_email = settings.DEFAULT_FROM_EMAIL,
                    recipient_list = [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error sending email: {e}")
                return Response(
                    {"message": "User registered successfully, but email could not be sent."},
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {"message": "User registered successfully. Confirmation email sent."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                # Now using the correct CustomUser model
                user = User.objects.get(email=email)
                user = authenticate(username=user.username, password=password)
                if user:
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        "message": "Login successful.",
                        "access": str(refresh.access_token),
                        "refresh": str(refresh)
                    }, status=status.HTTP_200_OK)
                return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetView(APIView):
    def post(self, request):
        serializer = RequestPasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()  # Send OTP via email
            if result:
                # Store email in session for future use
                request.session['reset_email'] = result['email']
                
                return Response({
                    "message": "OTP has been sent to your email."
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to send OTP email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerifyView(APIView):
    def post(self, request):
        # Get email from query parameters or session
        email = request.query_params.get('email') or request.session.get('reset_email')
        
        if not email:
            return Response({"error": "Email parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
            
        # Pass email in context
        serializer = OTPVerifySerializer(data=request.data, context={'email': email})
        if serializer.is_valid():
            user = serializer.save()  # OTP is verified and verification flag is set
            
            # Store email in session for use in password reset
            request.session['reset_email'] = user.email
            
            return Response({
                "message": "OTP verified successfully. You can now reset your password."
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    def post(self, request):
        # Extract email from query parameters or session
        email = request.query_params.get('email') or request.session.get('reset_email')
        
        if not email:
            return Response({"error": "Email parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
            
        # Pass email in context
        serializer = PasswordResetSerializer(data=request.data, context={'email': email})
        if serializer.is_valid():
            serializer.save()  # Password is reset
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected view."})