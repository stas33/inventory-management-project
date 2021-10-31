from django.db import models
import datetime
# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=50, blank=False, null=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    address = models.CharField(max_length=100, null=True)
    postcode = models.IntegerField(default='0', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name