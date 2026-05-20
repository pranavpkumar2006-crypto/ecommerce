from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.models import Address
from apps.cart.models import Wishlist
from apps.cart.utils import get_cart
from apps.catalog.models import Category, Product, Review
from apps.orders.models import Order

from .serializers import AddressSerializer, CartSerializer, CategorySerializer, OrderSerializer, ProductSerializer, ReviewSerializer, UserSerializer, WishlistSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related('category', 'brand').prefetch_related('images')
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        qs = super().get_queryset()
        if q := self.request.query_params.get('q'):
            qs = qs.filter(name__icontains=q)
        if category := self.request.query_params.get('category'):
            qs = qs.filter(category__slug=category)
        return qs


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(is_approved=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, is_approved=False)


class CartViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response(CartSerializer(get_cart(request)).data)


class WishlistViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        return Response(WishlistSerializer(wishlist).data)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items')


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False)
    def me(self, request):
        return Response(UserSerializer(request.user).data)
