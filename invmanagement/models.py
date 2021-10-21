from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

category_choice = (
        ('Pc', 'Pc'),
        ('Keyboard', 'Keyboard'),
        ('Phone', 'Phone'),
        ('Mouse', 'Mouse'),
        ('Speaker', 'Speaker'),
        ('Monitor', 'Monitor'),
        ('IT Equipment', 'IT Equipment'),
    )

STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
        ('Processing', 'Processing'),
        ('Delivered', 'Delivered'),
    )

#class Category(models.Model):
#    name = models.CharField(max_length=50, blank=True, null=True, choices=category_choice)
#    def __str__(self):
#        return self.name


class Product(models.Model):
    category = models.CharField(max_length=50, blank=True, choices=category_choice)
    prod_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=False, null=True)
    availability = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    #timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.prod_name


#class Customer(models.Model):
#    username = models.CharField(max_length=100, blank=False, null=True, unique=True)
#    phone = models.CharField(max_length=100, blank=False, null=True)
#    email = models.CharField(max_length=100, blank=False, null=True)
#    address = models.CharField(max_length=100, blank=False, null=True)
#    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)#
#
#    def __str__(self):
#        return self.username

#   @property
#    def orders(self):
#        order_count = self.order_set.all().count()
#        return str(order_count)


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='%(class)s_groups')
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, null=True, blank=True, choices=STATUS)
    quantity = models.IntegerField(default='0', blank=False, null=True)
    total_price = models.FloatField(max_length=50, null=True)

    def __str__(self):
        return str(self.product)

