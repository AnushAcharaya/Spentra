from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile
import logging

logger = logging.getLogger(__name__)

class UserProfileSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'full_name', 'photo', 'photo_url', 'first_name', 'last_name', 
            'gender', 'country', 'language', 'location', 'bio', 'date_updated', 'date_created'
        ]
        read_only_fields = ['id', 'date_updated', 'date_updated']
        
    def get_photo_url(self, obj):
        if obj.photo:
            try:
                return obj.photo.url
            except Exception as e:
                logger.error(f"Error getting photo URL: {str(e)}")
                return None
        return None
    
    def validate_photo(self, value):
        if value:
            # Check file size (2MB limit)
            if value.size > 2 * 1024 * 1024:
                raise serializers.ValidationError("Image file too large (max 2MB)")
                
            # Check file type
            if not value.content_type.startswith('image/'):
                raise serializers.ValidationError("Uploaded file is not an image")
                
        return value

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']
        read_only_fields = ['id', 'username']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        
        # Update user fields
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Ensure profile exists
        profile, created = UserProfile.objects.get_or_create(user=instance)
        
        # Update profile fields with proper error handling
        try:
            # Update each field individually with proper validation
            for attr, value in profile_data.items():
                if value is not None:  # Only update if value is provided
                    setattr(profile, attr, value)
            
            profile.save()
        except Exception as e:
            logger.error(f"Error updating profile: {str(e)}")
            raise serializers.ValidationError(f"Error updating profile: {str(e)}")

        return instance