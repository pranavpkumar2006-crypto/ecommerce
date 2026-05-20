from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReviewForm
from .models import Brand, Category, Product


def shop(request):
    products = Product.objects.filter(is_active=True).select_related('category', 'brand').prefetch_related('images')
    q = request.GET.get('q', '')
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(sku__icontains=q))
    if category := request.GET.get('category'):
        products = products.filter(category__slug=category)
    if brand := request.GET.get('brand'):
        products = products.filter(brand__slug=brand)
    if min_price := request.GET.get('min_price'):
        products = products.filter(price__gte=min_price)
    if max_price := request.GET.get('max_price'):
        products = products.filter(price__lte=max_price)
    if rating := request.GET.get('rating'):
        products = products.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=rating)
    sort = request.GET.get('sort', '-created_at')
    allowed = {'price', '-price', 'name', '-created_at'}
    products = products.order_by(sort if sort in allowed else '-created_at')
    page = Paginator(products, 12).get_page(request.GET.get('page'))
    return render(request, 'catalog/shop.html', {
        'page_obj': page,
        'categories': Category.objects.filter(is_active=True),
        'brands': Brand.objects.all(),
    })


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related('category', 'brand').prefetch_related('images', 'variants'), slug=slug, is_active=True)
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Review submitted for moderation.')
            return redirect(product)
    else:
        form = ReviewForm()
    related = Product.objects.filter(category=product.category, is_active=True).exclude(pk=product.pk)[:4]
    return render(request, 'catalog/product_detail.html', {'product': product, 'form': form, 'related': related})


def categories(request):
    return render(request, 'catalog/categories.html', {'categories': Category.objects.filter(is_active=True)})

# Create your views here.
