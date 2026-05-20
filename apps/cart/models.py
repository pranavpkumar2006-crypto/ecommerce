from decimal import Decimal

from django.conf import settings
from django.db import models

from apps.catalog.models import Product, ProductVariant


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    discount_percent = models.PositiveSmallIntegerField(default=0)
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    active = models.BooleanField(default=True)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    minimum_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def discount_for(self, subtotal):
        percent = subtotal * Decimal(self.discount_percent) / Decimal(100)
        return min(subtotal, max(percent, self.discount_amount))

    def __str__(self):
        return self.code


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='cart')
    session_key = models.CharField(max_length=80, blank=True, db_index=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def subtotal(self):
        return sum((item.line_total for item in self.items.select_related('product')), Decimal('0.00'))

    @property
    def discount_total(self):
        return self.coupon.discount_for(self.subtotal) if self.coupon and self.coupon.active else Decimal('0.00')

    @property
    def shipping_total(self):
        return Decimal('0.00') if self.subtotal >= Decimal('999.00') else Decimal('79.00')

    @property
    def total(self):
        return max(Decimal('0.00'), self.subtotal - self.discount_total + self.shipping_total)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product', 'variant')

    @property
    def unit_price(self):
        base = self.product.final_price
        return base + (self.variant.price_delta if self.variant else Decimal('0.00'))

    @property
    def line_total(self):
        return self.unit_price * self.quantity


class Wishlist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField(Product, blank=True, related_name='wishlisted_by')
    updated_at = models.DateTimeField(auto_now=True)

# Create your models here.
