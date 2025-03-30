import re
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
import random
from django.core.cache import cache
from django.utils.timezone import now, timedelta

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
        

    def validate_password(self, value):
        # Ensure the password contains uppercase, lowercase, digit, and special character
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
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




class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)

        # Generate a 6-digit OTP
        otp = random.randint(100000, 999999)

        # Store the OTP in the cache with a 10-minute expiration
        cache_key = f"password_reset_otp_{user.pk}"
        cache.set(cache_key, otp, timeout=600)  # 600 seconds = 10 minutes

        # Send the OTP via email
        send_mail(
            subject="Your Password Reset OTP",
            message=f"Your OTP for password reset is: {otp}. It is valid for 10 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )





class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')
        new_password = attrs.get('new_password')

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

        # Validate the new password (optional, based on your requirements)
        validate_password(new_password, user)

        return attrs

    def save(self):
        email = self.validated_data['email']
        new_password = self.validated_data['new_password']

        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        # Clear the OTP from the cache
        cache_key = f"password_reset_otp_{user.pk}"
        cache.delete(cache_key)