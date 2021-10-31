from django.db import models
from django.contrib.auth import get_user_model
import datetime
from django.contrib.auth.models import User
from products.models import Product
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
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='%(class)s_groups')
    #customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    #date_created = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(default=datetime.datetime.today)
    status = models.CharField(max_length=50, null=True, blank=True, choices=STATUS)
    quantity = models.IntegerField(default='0', blank=False, null=True)
    price = models.FloatField(max_length=50, null=True)
    phone = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.product)

    def get_order_by_customer(user_id):
        return Order.objects.filter(user=user_id,
                                    user__groups__name='customer')