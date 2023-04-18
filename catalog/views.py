from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from .models import Item, OrderItem, Order
from django.contrib import messages
from django.utils import timezone
from django.views import View


class HomeView(ListView):
    model = Item 
    template_name = 'home.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Item
    template_name = 'product.html'
    context_object_name = 'product'


class AddToCartView(View):
    def get(self, request, slug):
        item = get_object_or_404(Item, slug=slug)
        order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug):
                order_item.quantity += 1
                order_item.save()
                messages.success(request, f"{item.title}'s quantity was successfully updated in cart")
                return redirect('product', slug=slug)
            else:
                order.items.add(order_item)
                order.save()
                messages.success(request, f"{item.title} was successfully added to cart")
                return redirect('product', slug=slug)
            
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(user=request.user, ordered=False, ordered_date=ordered_date)
            order.items.add(order_item)
            order.save()
            messages.success(request, f"{item.title} was successfully added to cart")
            return redirect('product', slug=slug)

    def post(self, request, slug):
        return self.get(request, slug)
        
        
        
    
    
    

