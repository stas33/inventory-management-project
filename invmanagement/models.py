from django.db import models

category_choice = (
    ('Pc', 'Pc'),
    ('Keyboard', 'Keyboard'),
    ('Phone', 'Phone'),
    ('Mouse', 'Mouse'),
    ('Speaker', 'Speaker'),
    ('Monitor', 'Monitor'),
    ('IT Equipment', 'IT Equipment'),
)

class Category(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    prod_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=False, null=True)
    availability = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    #timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.category + ' , quantity: ' + str(self.quantity)
