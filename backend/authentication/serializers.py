import re
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.conf import settings
import random
from django.core.cache import cache
from .models import CustomUser


"""_summary_
    
        This module defines serializers for user authentication and profile management in the Spentra application.
        It includes serializers for user registration, login, password reset, and OTP verification.
        The serializers handle validation and serialization of user data, including password complexity requirements.
        The OTP verification process is also included to enhance security during password resets.
        The RegisterSerializer ensures that the password meets specific criteria, including the presence of uppercase letters,
        lowercase letters, digits, and special characters. It also checks for matching passwords during registration.
        The LoginSerializer handles user login, while the PasswordResetSerializer manages password reset requests and validation.
        The OTPVerifySerializer is used to verify the OTP sent to the user's email during the password reset process.
        

"""
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        help_text="Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')

    def validate_email(self, value):
        # Ensure the email contains "@" and at least one digit
        if not re.search(r'@', value):
            raise serializers.ValidationError("Email must contain '@'.")
        return value

    def validate_password(self, value):
        # Ensure the password contains uppercase, lowercase, digit, and special character
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return value

    def validate(self, attrs):
        # Ensure passwords match
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")
        return data


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        
        # Generate OTP (6-digit number)
        otp = random.randint(100000, 999999)
        
        # Store OTP in cache with 10-minute expiration
        cache_key = f"password_reset_otp_{user.pk}"
        cache.set(cache_key, otp, timeout=600)  # 600 seconds = 10 minutes
        
        # Send OTP via email
        try:
            send_mail(
                subject='Password Reset OTP',
                message=f'Your OTP for password reset is: {otp}. This OTP is valid for 10 minutes.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            return {'email': email, 'user': user}
        except Exception as e:
            print(f"Error sending email: {e}")
            return None


class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.IntegerField()

    def validate(self, attrs):
        otp = attrs.get('otp')
        
        # Get email from context (will be passed from the view)
        email = self.context.get('email')
        if not email:
            raise serializers.ValidationError("Email context is required")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

        # Retrieve the OTP from the cache
        cache_key = f"password_reset_otp_{user.pk}"
        cached_otp = cache.get(cache_key)

        if cached_otp is None:
            raise serializers.ValidationError("OTP has expired or is invalid.")
        if cached_otp != otp:
            raise serializers.ValidationError("Invalid OTP.")
            
        # Store email for use in save method
        attrs['email'] = email

        return attrs

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)

        # Clear the OTP from the cache after successful verification
        cache_key = f"password_reset_otp_{user.pk}"
        cache.delete(cache_key)
        
        # Set a verification flag that will be checked during password reset
        verification_key = f"password_reset_verified_{user.pk}"
        cache.set(verification_key, True, timeout=600)  # 10 minutes to complete password reset

        return user


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        
        # Get email from context (will be passed from the view)
        email = self.context.get('email')
        if not email:
            raise serializers.ValidationError("Email is required")
            
        # Check if user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

        # Check if OTP was verified
        cache_key = f"password_reset_verified_{user.pk}"
        verified = cache.get(cache_key)
        if not verified:
            raise serializers.ValidationError("Please verify your OTP first.")

        # Validate password complexity
        if not re.search(r'[A-Z]', new_password):
            raise serializers.ValidationError({"new_password": "Password must contain at least one uppercase letter."})
        if not re.search(r'[a-z]', new_password):
            raise serializers.ValidationError({"new_password": "Password must contain at least one lowercase letter."})
        if not re.search(r'\d', new_password):
            raise serializers.ValidationError({"new_password": "Password must contain at least one digit."})
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', new_password):
            raise serializers.ValidationError({"new_password": "Password must contain at least one special character."})

        # Check if passwords match
        if new_password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Password fields didn't match."})

        # Validate the new password
        validate_password(new_password, user)
        
        # Store email for use in save method
        attrs['email'] = email
        
        return attrs

    def save(self):
        email = self.validated_data['email']
        new_password = self.validated_data['new_password']

        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        # Clear verification flag from cache
        cache_key = f"password_reset_verified_{user.pk}"
        cache.delete(cache_key)
        
        return user


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'