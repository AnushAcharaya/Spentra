from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer,PasswordResetSerializer
from django.core.mail import send_mail
from django.conf import settings

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
                user = User.objects.get(email=email)
                user = authenticate(username=user.username, password=password)
                if user:
                    return Response({"message": "Login successful."}, status=status.HTTP_200_OK)
                return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PasswordResetSerializer


class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()  # This will generate and send the OTP
                return Response(
                    {"message": "OTP has been sent to your email."},
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                print(f"Error sending OTP email: {e}")
                return Response(
                    {"error": "An error occurred while sending the OTP. Please try again later."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)