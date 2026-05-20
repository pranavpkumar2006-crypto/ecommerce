from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from django.shortcuts import render

from apps.catalog.models import Product
from apps.orders.models import Order


@staff_member_required
def admin_dashboard(request):
    revenue = Order.objects.exclude(status=Order.CANCELLED).aggregate(total=Sum('grand_total'))['total'] or 0
    context = {
        'revenue': revenue,
        'orders': Order.objects.count(),
        'products': Product.objects.count(),
        'latest_orders': Order.objects.select_related('user')[:8],
        'status_counts': Order.objects.values('status').annotate(total=Count('id')),
    }
    return render(request, 'admin/dashboard.html', context)
