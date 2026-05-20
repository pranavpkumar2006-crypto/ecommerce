from django.conf import settings


def create_stripe_checkout(order):
    if not settings.STRIPE_SECRET_KEY:
        return {'configured': False, 'message': 'Stripe keys are not configured.'}
    import stripe

    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe.checkout.Session.create(
        payment_method_types=['card'],
        mode='payment',
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {'name': f'Order {order.order_number}'},
                'unit_amount': int(order.grand_total * 100),
            },
            'quantity': 1,
        }],
        success_url='/orders/payment/success/',
        cancel_url='/orders/payment/failure/',
    )


def create_razorpay_order(order):
    if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
        return {'configured': False, 'message': 'Razorpay keys are not configured.'}
    import razorpay

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    return client.order.create({
        'amount': int(order.grand_total * 100),
        'currency': 'INR',
        'receipt': order.order_number,
        'payment_capture': 1,
    })
