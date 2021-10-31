from django.db import models
import datetime

# Create your models here.
category_choice = (
        ('Pc', 'Pc'),
        ('Keyboard', 'Keyboard'),
        ('Phone', 'Phone'),
        ('Mouse', 'Mouse'),
        ('Speaker', 'Speaker'),
        ('Monitor', 'Monitor'),
        ('IT Equipment', 'IT Equipment'),
    )


class Product(models.Model):
    category = models.CharField(max_length=50, blank=False, choices=category_choice)
    prod_name = models.CharField(max_length=50, blank=False, null=True)
    quantity = models.IntegerField(default='0', blank=False, null=True)
    availability = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    price = models.IntegerField(default=0, blank=False)
    #timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.prod_name

    def get_products_by_id(cart_product_id):
        return Product.objects.filter(id__in=cart_product_id)