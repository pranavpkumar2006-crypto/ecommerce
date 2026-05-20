from uuid import uuid4

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.accounts.models import Address
from apps.cart.utils import get_cart
from services.payments import create_razorpay_order, create_stripe_checkout
from utils.invoices import render_invoice_pdf

from .models import Order, OrderItem, Payment, ReturnRequest


@login_required
def checkout(request):
    cart = get_cart(request)
    addresses = request.user.addresses.all()
    if not cart.items.exists():
        messages.info(request, 'Your cart is empty.')
        return redirect('cart')
    if request.method == 'POST':
        shipping = get_object_or_404(Address, pk=request.POST.get('shipping_address'), user=request.user)
        billing = get_object_or_404(Address, pk=request.POST.get('billing_address'), user=request.user)
        order = Order.objects.create(
            user=request.user,
            order_number=uuid4().hex[:12].upper(),
            shipping_address=shipping,
            billing_address=billing,
            payment_method=request.POST.get('payment_method', 'cod'),
            discount_total=cart.discount_total,
            shipping_total=cart.shipping_total,
        )
        for item in cart.items.select_related('product', 'variant'):
            OrderItem.objects.create(
                order=order,
                product=item.product,
                variant=item.variant,
                name=item.product.name,
                sku=item.variant.sku if item.variant else item.product.sku,
                price=item.unit_price,
                quantity=item.quantity,
            )
        order.calculate_totals()
        order.save()
        cart.items.all().delete()
        if order.payment_method == 'stripe':
            session = create_stripe_checkout(order)
            Payment.objects.create(order=order, provider='stripe', raw_response=dict(session))
        elif order.payment_method == 'razorpay':
            rz_order = create_razorpay_order(order)
            Payment.objects.create(order=order, provider='razorpay', provider_order_id=rz_order.get('id', ''), raw_response=rz_order)
        messages.success(request, 'Order placed successfully.')
        return redirect('order_detail', order_number=order.order_number)
    return render(request, 'orders/checkout.html', {'cart': cart, 'addresses': addresses})


@login_required
def orders(request):
    return render(request, 'orders/orders.html', {'orders': request.user.orders.all()})


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(request.user.orders.prefetch_related('items'), order_number=order_number)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
@require_POST
def cancel_order(request, order_number):
    order = get_object_or_404(request.user.orders, order_number=order_number)
    if order.status in [Order.PENDING, Order.PROCESSING]:
        order.status = Order.CANCELLED
        order.save()
        messages.info(request, 'Order cancelled.')
    return redirect('order_detail', order_number=order.order_number)


@login_required
@require_POST
def request_return(request, order_number):
    order = get_object_or_404(request.user.orders, order_number=order_number, status=Order.DELIVERED)
    ReturnRequest.objects.create(order=order, reason=request.POST.get('reason', 'Return requested'))
    messages.success(request, 'Return request submitted.')
    return redirect('order_detail', order_number=order.order_number)


@login_required
def invoice(request, order_number):
    order = get_object_or_404(request.user.orders.prefetch_related('items'), order_number=order_number)
    return FileResponse(render_invoice_pdf(order), as_attachment=True, filename=f'invoice-{order.order_number}.pdf')


def payment_success(request):
    messages.success(request, 'Payment completed.')
    return redirect('orders')


def payment_failure(request):
    messages.error(request, 'Payment failed or was cancelled.')
    return redirect('orders')

# Create your views here.
