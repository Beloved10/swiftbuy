from django.db import models
from django.contrib.auth.models import User


CATEGORY_CHOICES = (
    ('SH', 'Shirts'),
    ('TR', 'Trousers'),
    ('FW', 'Footwears'),
    ('OT', 'Others'),
    ('WT', 'Watches'),
    ('GT', 'Gadgets')
)

LABEL_CHOICES = (
    ('secondary', 'Top'),
    ('primary', 'Trending'),
    ('danger', 'New')
)

class Item(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    slug = models.SlugField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=15)
    label = models.CharField(choices=LABEL_CHOICES, max_length=15)
    description = models.TextField()
    image = models.ImageField(default='default.jpg', upload_to='static/images')
    
    def __str__(self):
        return self.title
    

class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    
    
    def __str__(self):
        return f"{self.quantity} of {self.item.title} by {self.user.username}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    
    def __str__(self):
        return self.user.username
