from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Item, OrderItem, Order


class HomeView(ListView):
    model = Item 
    template_name = 'home.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Item
    template_name = 'product.html'
    context_object_name = 'product'

def checkout(request):
    return render(request, 'checkout.html')

