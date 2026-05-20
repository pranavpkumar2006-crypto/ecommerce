from django.urls import path

from . import views

urlpatterns = [
    path('shop/', views.shop, name='shop'),
    path('categories/', views.categories, name='categories'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]
