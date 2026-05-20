from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    CUSTOMER = 'customer'
    STAFF = 'staff'
    VENDOR = 'vendor'
    ROLE_CHOICES = [(CUSTOMER, 'Customer'), (STAFF, 'Staff'), (VENDOR, 'Vendor')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CUSTOMER)
    phone = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_username()


class Address(models.Model):
    SHIPPING = 'shipping'
    BILLING = 'billing'
    TYPE_CHOICES = [(SHIPPING, 'Shipping'), (BILLING, 'Billing')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=80, default='India')
    address_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=SHIPPING)
    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_default', 'city']

    def __str__(self):
        return f'{self.full_name}, {self.city}'

# Create your models here.
