from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True, null=True)
    photo = models.ImageField(
        upload_to="profile_photos/", 
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(
        max_length=10, 
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], 
        blank=True, 
        null=True
    )
    country = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def clean(self):
        # Restrict file size (e.g., 2 MB)
        max_file_size = 2 * 1024 * 1024  # 2 MB in bytes
        if self.photo and self.photo.size > max_file_size:
            raise ValidationError("The uploaded file is too large. Maximum size allowed is 2 MB.")

        # Ensure the file is an image
        if self.photo and hasattr(self.photo, 'file') and not self.photo.file.content_type.startswith('image/'):
            raise ValidationError("The uploaded file must be an image (JPEG, PNG, etc.).")

    def save(self, *args, **kwargs):
        # Auto-populate full_name if first and last name are provided but full_name is not
        if not self.full_name and self.first_name and self.last_name:
            self.full_name = f"{self.first_name} {self.last_name}"
        elif not self.full_name:
            # Fallback to username if no names are provided
            self.full_name = self.user.username
            
        # Clean before saving
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name or self.user.username