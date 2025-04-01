from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)

    def clean(self):
        # Restrict file size (e.g., 2 MB)
        max_file_size = 2 * 1024 * 1024  # 2 MB in bytes
        if self.photo and self.photo.size > max_file_size:
            raise ValidationError("The uploaded file is too large. Maximum size allowed is 2 MB.")

        # Ensure the file is an image
        if self.photo and not self.photo.file.content_type.startswith('image/'):
            raise ValidationError("The uploaded file must be an image (JPEG, PNG, etc.).")

    def __str__(self):
        return self.full_name