from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from .models import Item, OrderItem, Order
from django.contrib import messages
from django.utils import timezone
from django.views import View


class HomeView(View):

    def get(self, request, *args, **kwargs):
        # Get all items from the Item model
        products = Item.objects.all()

        # Get the current user's cart items, assuming the user is logged in via admin panel
        # You can update this logic as per your authentication implementation
        if request.user.is_authenticated:
        # Assuming Order model has a one-to-one relationship with User model
        # You can adjust the relationship based on your actual model structure
            order = Order.objects.filter(user=request.user, ordered=False).first()
            if order:
                # Count only the OrderItems that are still associated with the Order
                cart_count = order.items.filter(ordered=False).count()
            else:
                cart_count = 0
        else:
            cart_count = 0
            
        context = {
            'products': products,
            'cart_count': cart_count
        }
        return render(request, 'home.html', context)


        # Add cart_items_count to the context
       



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
    
    
    
class RemoveItemFromCartView(View):
    def get(self, request, slug):
        item = get_object_or_404(Item, slug=slug)
        order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item.delete()  # Remove the item from OrderItem table
                order.save()
                messages.success(request, f"{item.title} was successfully removed from your cart")
                return redirect('product', slug=slug)
            else:
                messages.info(request, f"{item.title} was not in your cart")
                return redirect('product', slug=slug)
        else:
            messages.info(request, "You do not have an active order!")
            return redirect('product', slug=slug)

    def post(self, request, slug):
        return self.get(request, slug)
    
class CartView(View):
    def get(self, request, *args, **kwargs):
        cart = None
        cart_total = 0
        if request.user.is_authenticated:
            # Assuming Order model has a one-to-one relationship with User model
            # You can adjust the relationship based on your actual model structure
            order = Order.objects.filter(user=request.user, ordered=False).first()
            if order:
                # Count only the OrderItems that are still associated with the Order
                cart = order.items.filter(ordered=False)
                # Calculate the total amount for checked items in the cart
                checked_items = request.GET.getlist('items')  # Get the list of checked items from query parameters
                cart_total = sum(item.item.price * item.quantity for item in cart if str(item.item.slug) in checked_items)
            else:
                messages.info(request, 'You have no item in your cart!')
        else:
            messages.info(request, 'Please sign in to view your cart')

        context = {'cart': cart, 'cart_total': cart_total}
        return render(request, 'cart.html', context)
        
    
    
    

