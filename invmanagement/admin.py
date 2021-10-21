from django.contrib import admin
from .models import *
from .forms import CreateProductForm

# Register your models here.

class CreateProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'prod_name', 'quantity']
    form = CreateProductForm
    list_filter = ['category']
    search_fields = ['category', 'prod_name']

admin.site.register(Product, CreateProductAdmin)
#admin.site.register(Category)
#admin.site.register(Customer)
admin.site.register(Order)
