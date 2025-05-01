from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import UserProfile
import tempfile
from PIL import Image
import json

def create_test_image():
    """Create a test image file for testing uploads"""
    image = Image.new('RGB', (100, 100), color='red')
    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(tmp_file)
    tmp_file.seek(0)
    return tmp_file

class UserProfileAPITestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        # Create regular user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Create admin user
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpassword123',
            is_staff=True,
            is_superuser=True
        )
        
        # Set up clients
        self.client = APIClient()
        self.user_client = APIClient()
        self.user_client.force_authenticate(user=self.user)
        
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(user=self.admin)
        
        # Create a profile (should be created by signals)
        self.profile = UserProfile.objects.get(user=self.user)
        self.profile.full_name = "Test User"
        self.profile.save()
        
        # URLs
        self.profile_url = reverse('user-profile')
    
    def test_get_profile_authenticated(self):
        """Test retrieving profile when authenticated"""
        response = self.user_client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'Test User')
    
    def test_get_profile_unauthenticated(self):
        """Test retrieving profile when not authenticated"""
        response = self.client.get(self.profile_url)
        # This will return 401 or demo data depending on DEBUG setting
        if response.status_code == status.HTTP_200_OK:
            # In DEBUG mode
            self.assertEqual(response.data['full_name'], 'Demo User')
        else:
            # Not in DEBUG mode
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_profile_authenticated(self):
        """Test updating profile when authenticated"""
        update_data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'country': 'Test Country'
        }
        response = self.user_client.put(
            self.profile_url,
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Updated')
        self.assertEqual(response.data['last_name'], 'User')
        self.assertEqual(response.data['country'], 'Test Country')
        
        # Verify database was updated
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.first_name, 'Updated')

    def test_update_profile_unauthenticated(self):
        """Test updating profile when not authenticated"""
        update_data = {
            'first_name': 'Should',
            'last_name': 'Fail'
        }
        response = self.client.put(
            self.profile_url,
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Verify database was not updated
        self.profile.refresh_from_db()
        self.assertNotEqual(self.profile.first_name, 'Should')
    
    def test_photo_upload(self):
        """Test uploading a profile photo"""
        with create_test_image() as image_file:
            response = self.user_client.put(
                self.profile_url,
                {'photo': image_file},
                format='multipart'
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIsNotNone(response.data['photo_url'])
            
            # Verify photo was saved
            self.profile.refresh_from_db()
            self.assertTrue(self.profile.photo)
    
    def test_invalid_data(self):
        """Test validation of invalid data"""
        # Test invalid gender
        invalid_data = {'gender': 'invalid_gender'}
        response = self.user_client.put(
            self.profile_url,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)