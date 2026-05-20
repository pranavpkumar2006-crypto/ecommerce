# CommercePro Django eCommerce

Full-stack eCommerce platform built with Django, Django REST Framework, Bootstrap 5, vanilla JavaScript, SQLite for development, and PostgreSQL-ready production settings.

## Features

- Authentication: registration, login/logout, password reset, email verification hook, profiles, addresses, image upload.
- Storefront: homepage carousel, featured products, categories, best sellers, latest arrivals, offers, testimonials, newsletter, SEO sitemap and robots.txt.
- Catalog: products, slugs, SKU, brand, category/subcategory, tags, variants, multiple images, reviews, ratings, filters, sorting, pagination.
- Cart and wishlist: persisted user cart, session cart, AJAX quantity updates, coupons, shipping calculation.
- Checkout: shipping/billing addresses, order snapshots, tax/shipping/discount totals, COD, Stripe and Razorpay integration points.
- Orders: tracking, cancellation, return requests, downloadable PDF invoices, admin CSV export.
- Admin: model management, review moderation, coupons, banners, inventory fields, and `/admin/dashboard/` analytics.
- API: `/api/products/`, `/api/categories/`, `/api/cart/`, `/api/orders/`, `/api/wishlist/`, `/api/addresses/`, `/api/auth/me/`.

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Production Notes

Set environment variables from `.env.example`, use PostgreSQL, run `collectstatic`, serve through Gunicorn and Nginx using the files in `deploy/`, and configure SMTP plus real Stripe/Razorpay webhook verification before accepting live payments.

```bash
python manage.py collectstatic
gunicorn config.wsgi:application -c deploy/gunicorn.conf.py
```

Security defaults include CSRF middleware, Django ORM protection, password validators, clickjacking protection, content-type sniffing protection, HTTP-only session cookies, and DRF permission controls.
