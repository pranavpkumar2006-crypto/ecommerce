from django.contrib import admin

from .models import Banner, NewsletterSubscriber, Testimonial


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'sort_order']
    list_editable = ['is_active', 'sort_order']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'is_active']
    list_editable = ['is_active']


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_at']

# Register your models here.
