from decimal import Decimal

from django.conf import settings
from django.db import models

from apps.accounts.models import Address
from apps.catalog.models import Product, ProductVariant


class Order(models.Model):
    PENDING = 'pending'
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
    RETURNED = 'returned'
    STATUS_CHOICES = [
        (PENDING, 'Pending'), (PROCESSING, 'Processing'), (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'), (CANCELLED, 'Cancelled'), (RETURNED, 'Returned'),
    ]
    PAYMENT_CHOICES = [('cod', 'Cash on Delivery'), ('stripe', 'Stripe'), ('razorpay', 'Razorpay')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='orders')
    order_number = models.CharField(max_length=24, unique=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='shipping_orders')
    billing_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='billing_orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cod')
    payment_status = models.CharField(max_length=30, default='unpaid')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tracking_number = models.CharField(max_length=80, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def calculate_totals(self):
        self.subtotal = sum((item.line_total for item in self.items.all()), Decimal('0.00'))
        self.tax_total = (self.subtotal - self.discount_total) * Decimal('0.18')
        self.grand_total = self.subtotal - self.discount_total + self.tax_total + self.shipping_total

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=180)
    sku = models.CharField(max_length=80)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def line_total(self):
        return self.price * self.quantity


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    provider = models.CharField(max_length=20)
    provider_order_id = models.CharField(max_length=120, blank=True)
    provider_payment_id = models.CharField(max_length=120, blank=True)
    signature = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=30, default='created')
    raw_response = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ReturnRequest(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='return_requests')
    reason = models.TextField()
    status = models.CharField(max_length=30, default='requested')
    created_at = models.DateTimeField(auto_now_add=True)

# Create your models here.
