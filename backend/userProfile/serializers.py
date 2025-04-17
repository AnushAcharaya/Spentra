from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'full_name', 'photo', 'first_name', 'last_name', 'gender', 
            'country', 'language', 'location', 'bio'
        ]  # Include new fields

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        full_name = profile_data.get('full_name')
        photo = profile_data.get('photo')
        first_name = profile_data.get('first_name')
        last_name = profile_data.get('last_name')
        gender = profile_data.get('gender')
        country = profile_data.get('country')
        language = profile_data.get('language')
        location = profile_data.get('location')
        bio = profile_data.get('bio')

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile = instance.profile
        if full_name:
            profile.full_name = full_name
        if photo:
            profile.photo = photo
        if first_name:
            profile.first_name = first_name
        if last_name:
            profile.last_name = last_name
        if gender:
            profile.gender = gender
        if country:
            profile.country = country
        if language:
            profile.language = language
        if location:
            profile.location = location
        if bio:
            profile.bio = bio
        profile.save()

        return instance