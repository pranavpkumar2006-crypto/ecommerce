from django.db import models


class Banner(models.Model):
    title = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='banners/', blank=True, null=True)
    cta_label = models.CharField(max_length=40, default='Shop now')
    cta_url = models.CharField(max_length=255, default='/shop/')
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_active = models.BooleanField(default=True)


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Create your models here.
