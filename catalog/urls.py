from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product'),
    path('checkout', views.checkout, name='checkout'),
]