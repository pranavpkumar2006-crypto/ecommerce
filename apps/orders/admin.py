import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Order, OrderItem, Payment, ReturnRequest


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['line_total']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'payment_method', 'payment_status', 'grand_total', 'created_at']
    list_filter = ['status', 'payment_method', 'payment_status']
    search_fields = ['order_number', 'user__username', 'tracking_number']
    inlines = [OrderItemInline]
    actions = ['export_csv']

    @admin.action(description='Export selected orders as CSV')
    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=orders.csv'
        writer = csv.writer(response)
        writer.writerow(['Order', 'User', 'Status', 'Total', 'Created'])
        for order in queryset:
            writer.writerow([order.order_number, order.user.username, order.status, order.grand_total, order.created_at])
        return response


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'provider', 'status', 'provider_payment_id', 'created_at']


@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ['order', 'status', 'created_at']

# Register your models here.
