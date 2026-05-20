from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('newsletter/', views.newsletter_signup, name='newsletter_signup'),
    path('about/', views.flat_page, {'template': 'about'}, name='about'),
    path('contact/', views.flat_page, {'template': 'contact'}, name='contact'),
    path('faq/', views.flat_page, {'template': 'faq'}, name='faq'),
    path('privacy/', views.flat_page, {'template': 'privacy'}, name='privacy'),
    path('terms/', views.flat_page, {'template': 'terms'}, name='terms'),
]
