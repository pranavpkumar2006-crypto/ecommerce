from django.contrib import messages
from django.db.models import Count
from django.shortcuts import redirect, render

from apps.catalog.models import Category, Product

from .models import Banner, NewsletterSubscriber, Testimonial


def home(request):
    trending_products = Product.objects.filter(is_active=True).select_related('category', 'brand')[:10]
    context = {
        'banners': Banner.objects.filter(is_active=True),
        'featured_products': Product.objects.filter(is_active=True, is_featured=True).select_related('category', 'brand')[:8],
        'best_sellers': Product.objects.filter(is_active=True, is_best_seller=True).select_related('category', 'brand')[:8],
        'latest_products': Product.objects.filter(is_active=True).select_related('category', 'brand')[:8],
        'trending_products': trending_products,
        'recommended_products': Product.objects.filter(is_active=True).order_by('?')[:6],
        'categories': Category.objects.filter(is_active=True, parent__isnull=True).annotate(total=Count('products'))[:8],
        'testimonials': Testimonial.objects.filter(is_active=True)[:6],
    }
    return render(request, 'marketing/home.html', context)


def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            NewsletterSubscriber.objects.get_or_create(email=email)
            messages.success(request, 'Thanks for subscribing.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def flat_page(request, template):
    return render(request, f'marketing/{template}.html')

# Create your views here.
