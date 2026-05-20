from django.core.management.base import BaseCommand

from apps.catalog.models import Brand, Category, Product
from apps.marketing.models import Banner, Testimonial


class Command(BaseCommand):
    help = 'Create demo catalog, banner, and testimonial data.'

    def handle(self, *args, **options):
        category, _ = Category.objects.get_or_create(name='Electronics')
        fashion, _ = Category.objects.get_or_create(name='Fashion')
        brand, _ = Brand.objects.get_or_create(name='CommercePro')
        products = [
            ('Wireless Headphones', 'CP-AUD-100', category, 2499, 1999, True, True),
            ('Smart Watch', 'CP-WAT-200', category, 4999, 3499, True, False),
            ('Premium Backpack', 'CP-BAG-300', fashion, 1899, 1499, False, True),
            ('Everyday Sneakers', 'CP-SHO-400', fashion, 2999, 2499, True, True),
        ]
        for name, sku, cat, price, sale, featured, best in products:
            Product.objects.get_or_create(
                sku=sku,
                defaults={
                    'name': name,
                    'description': 'A premium, reliable product built for daily use.',
                    'price': price,
                    'discount_price': sale,
                    'stock_quantity': 50,
                    'category': cat,
                    'brand': brand,
                    'is_featured': featured,
                    'is_best_seller': best,
                },
            )
        Banner.objects.get_or_create(title='Big Store Sale', defaults={'subtitle': 'Fresh deals across electronics, fashion, and essentials.'})
        Testimonial.objects.get_or_create(name='Aarav Sharma', defaults={'message': 'Fast checkout, clean experience, and reliable delivery.', 'rating': 5})
        self.stdout.write(self.style.SUCCESS('Demo data created.'))
