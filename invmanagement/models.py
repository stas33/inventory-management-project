from django.db import models
from django.contrib.auth import get_user_model
import datetime
from django.contrib.auth.models import User

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

class Product(models.Model):
    category = models.CharField(max_length=50, blank=True, choices=category_choice)
    prod_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=False, null=True)
    availability = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    price = models.IntegerField(default=0, blank=False)
    #timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.prod_name

    def get_products_by_id(cart_product_id):
        return Product.objects.filter(id__in=cart_product_id)


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

    def does_exits(self):
        return Customer.objects.filter(email=self.email)

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

class Company(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    address = models.CharField(max_length=100, null=True)
    postcode = models.IntegerField(default='0', blank=True, null=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


