from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AddressViewSet, CartViewSet, CategoryViewSet, MeViewSet, OrderViewSet, ProductViewSet, ReviewViewSet, WishlistViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='api-products')
router.register('categories', CategoryViewSet, basename='api-categories')
router.register('reviews', ReviewViewSet, basename='api-reviews')
router.register('cart', CartViewSet, basename='api-cart')
router.register('wishlist', WishlistViewSet, basename='api-wishlist')
router.register('orders', OrderViewSet, basename='api-orders')
router.register('addresses', AddressViewSet, basename='api-addresses')
router.register('auth', MeViewSet, basename='api-auth')

urlpatterns = [path('', include(router.urls))]
