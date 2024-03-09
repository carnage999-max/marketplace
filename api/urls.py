from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ApiOverview, name='apiOverview'),
    path('users/', views.getusers, name='users'),
    path('ads/', views.get_products, name='ads'),
    
    path("accounts/", include('rest_registration.api.urls')),
]
