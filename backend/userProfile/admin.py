from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'gender', 'country', 'date_updated')
    search_fields = ('user__username', 'full_name', 'email', 'country')
    list_filter = ('gender', 'country', 'language')
    readonly_fields = ('date_created', 'date_updated')
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'full_name', 'email', 'photo')
        }),
        ('Personal Details', {
            'fields': ('first_name', 'last_name', 'gender', 'country', 'language', 'location')
        }),
        ('Additional Information', {
            'fields': ('bio', 'date_created', 'date_updated')
        }),
    )