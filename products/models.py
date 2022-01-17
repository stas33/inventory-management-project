from django.db import models
import datetime

class Category(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.name


class Product(models.Model):
    #category = models.CharField(max_length=50, blank=False, choices=category_choice)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=False, null=True)
    prod_name = models.CharField(max_length=50, blank=False, null=True)
    quantity = models.IntegerField(default='0', blank=False, null=True)
    availability = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    price = models.IntegerField(default=0, blank=False)
    image = models.ImageField(null=True, blank=True)
    #timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.prod_name

    def get_products_by_id(cart_product_id):
        return Product.objects.filter(id__in=cart_product_id)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url