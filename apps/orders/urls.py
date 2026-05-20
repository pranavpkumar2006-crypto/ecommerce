from django.urls import path

from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),
    path('orders/<str:order_number>/', views.order_detail, name='order_detail'),
    path('orders/<str:order_number>/cancel/', views.cancel_order, name='cancel_order'),
    path('orders/<str:order_number>/return/', views.request_return, name='request_return'),
    path('orders/<str:order_number>/invoice/', views.invoice, name='invoice'),
    path('orders/payment/success/', views.payment_success, name='payment_success'),
    path('orders/payment/failure/', views.payment_failure, name='payment_failure'),
]
