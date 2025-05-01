from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile instance when a new User is created."""
    if created:
        try:
            UserProfile.objects.create(
                user=instance,
                full_name=instance.username,  # Use the username as the full name initially
                email=instance.email          # Retrieve the email from the User model
            )
            logger.info(f"Created new profile for user {instance.username}")
        except Exception as e:
            logger.error(f"Error creating profile for user {instance.username}: {str(e)}")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile instance when the User is saved."""
    try:
        # Check if profile exists, create if it doesn't
        if not hasattr(instance, 'profile'):
            UserProfile.objects.create(
                user=instance,
                full_name=instance.username,
                email=instance.email
            )
            logger.info(f"Created missing profile for existing user {instance.username}")
        else:
            instance.profile.save()
            logger.info(f"Updated profile for user {instance.username}")
    except Exception as e:
        logger.error(f"Error saving profile for user {instance.username}: {str(e)}")