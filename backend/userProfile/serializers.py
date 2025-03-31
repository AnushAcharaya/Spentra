from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'photo']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        full_name = profile_data.get('full_name')
        photo = profile_data.get('photo')

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile = instance.profile
        if full_name:
            profile.full_name = full_name
        if photo:
            profile.photo = photo
        profile.save()

        return instance