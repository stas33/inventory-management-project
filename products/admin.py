from django.contrib import admin
from .models import *
from .forms import CreateProductForm
# Register your models here.

#
# class CreateProductAdmin(admin.ModelAdmin):
#     list_display = ['category', 'prod_name', 'quantity', 'price', 'availability', 'iamge']
#     form = CreateProductForm
#     list_filter = ['category']
#     search_fields = ['category', 'prod_name']

admin.site.register(Product)
admin.site.register(Category)