from django.contrib import admin

from .models import Address, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone', 'email_verified', 'created_at']
    list_filter = ['role', 'email_verified']
    search_fields = ['user__username', 'user__email', 'phone']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'city', 'state', 'address_type', 'is_default']
    list_filter = ['address_type', 'state', 'country']
    search_fields = ['full_name', 'phone', 'line1', 'city']

# Register your models here.
