from django.contrib import admin

from .models import Cart, CartItem, Coupon, Wishlist


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_key', 'coupon', 'updated_at']
    inlines = [CartItemInline]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'discount_amount', 'active', 'minimum_order_value']
    list_filter = ['active']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    filter_horizontal = ['products']

# Register your models here.
