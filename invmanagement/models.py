from django.db import models
from django.contrib.auth import get_user_model
import datetime
from django.contrib.auth.models import User
from companies.models import Company

User = get_user_model()


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.IntegerField(null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.name

    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

    def does_exits(self):
        return Customer.objects.filter(email=self.email)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.user
