from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.catalog.models import Product, ProductVariant

from .models import Coupon, Wishlist
from .utils import get_cart


def cart_detail(request):
    return render(request, 'cart/cart.html', {'cart': get_cart(request)})


@require_POST
def add_to_cart(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    variant = None
    if request.POST.get('variant_id'):
        variant = get_object_or_404(ProductVariant, pk=request.POST['variant_id'], product=product)
    item, created = cart.items.get_or_create(product=product, variant=variant)
    item.quantity = item.quantity + int(request.POST.get('quantity', 1)) if not created else int(request.POST.get('quantity', 1))
    item.save()
    messages.success(request, 'Added to cart.')
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'count': sum(i.quantity for i in cart.items.all()), 'total': str(cart.total)})
    return redirect('cart')


@require_POST
def update_cart_item(request, item_id):
    cart = get_cart(request)
    item = get_object_or_404(cart.items, pk=item_id)
    quantity = max(1, int(request.POST.get('quantity', 1)))
    item.quantity = quantity
    item.save()
    return JsonResponse({'line_total': str(item.line_total), 'cart_total': str(cart.total)})


@require_POST
def remove_cart_item(request, item_id):
    cart = get_cart(request)
    get_object_or_404(cart.items, pk=item_id).delete()
    return redirect('cart')


@require_POST
def apply_coupon(request):
    cart = get_cart(request)
    coupon = Coupon.objects.filter(code__iexact=request.POST.get('code', ''), active=True).first()
    if coupon and cart.subtotal >= coupon.minimum_order_value:
        cart.coupon = coupon
        cart.save()
        messages.success(request, 'Coupon applied.')
    else:
        messages.error(request, 'Coupon is invalid for this cart.')
    return redirect('cart')


@login_required
def wishlist(request):
    wishlist_obj, _ = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'cart/wishlist.html', {'wishlist': wishlist_obj})


@login_required
@require_POST
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    wishlist_obj, _ = Wishlist.objects.get_or_create(user=request.user)
    if product in wishlist_obj.products.all():
        wishlist_obj.products.remove(product)
        messages.info(request, 'Removed from wishlist.')
    else:
        wishlist_obj.products.add(product)
        messages.success(request, 'Added to wishlist.')
    return redirect(request.META.get('HTTP_REFERER', 'wishlist'))

# Create your views here.
