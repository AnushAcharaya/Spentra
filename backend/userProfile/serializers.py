from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')  # Map email to the User model's email field

    class Meta:
        model = UserProfile
        fields = ['full_name', 'email', 'photo']

    def validate_photo(self, value):
        # Restrict file size (e.g., 2 MB)
        max_file_size = 2 * 1024 * 1024  # 2 MB in bytes
        if value.size > max_file_size:
            raise ValidationError("The uploaded file is too large. Maximum size allowed is 2 MB.")

        # Ensure the file is an image
        if not value.content_type.startswith('image/'):
            raise ValidationError("The uploaded file must be an image (JPEG, PNG, etc.).")

        return value

    def update(self, instance, validated_data):
        # Update the email in the User model
        user_data = validated_data.pop('user', {})
        email = user_data.get('email')
        if email:
            instance.user.email = email
            instance.user.save()

        # Update the UserProfile fields
        return super().update(instance, validated_data)