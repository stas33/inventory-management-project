from django.db import models
from django.contrib.auth import get_user_model
import datetime
from django.contrib.auth.models import User
from products.models import Product
from invmanagement.models import *
# Create your models here.

STATUS = (
         ('Pending', 'Pending'),
         ('Approved', 'Approved'),
         ('Declined', 'Declined'),
         ('Processing', 'Processing'),
         ('Delivered', 'Delivered'),
     )


User = get_user_model()

class Order(models.Model):
    #product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True )
    #user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='%(class)s_groups')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    #date_created = models.DateTimeField(auto_now_add=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, null=True, blank=True, choices=STATUS)
    transaction_id = models.CharField(max_length=100, null=True)
    #quantity = models.IntegerField(default='0', blank=False, null=True)
    #price = models.FloatField(max_length=50, null=True)
    #phone = models.CharField(max_length=10, null=True)
    #address = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=False, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    # @property
    # def get_cart_quantity(self):
    #     #keys = cart.keys()
    #     keys = request.session.get('cart').keys()
    #     cart = request.session.get('cart')
    #     product = request.session.get('product')
    #     for id in keys:
    #         if int(id) == self.product.id:
    #             return cart.get(id)
    #     return 0

    # def orderitems_by_product_id(cart_product_id):
    #     return OrderItem.objects.filter(product__id__in=cart_product_id)

class Shipping(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=50, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address