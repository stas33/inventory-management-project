import django_filters
from .models import *

class ProductCustomerFilter(django_filters.FilterSet):
    prod_name = django_filters.CharFilter(label='Product name', lookup_expr='icontains')
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Product
        fields = ['prod_name']


class ProductSearchFilter(django_filters.FilterSet):
    prod_name = django_filters.CharFilter(label='Product name', lookup_expr='icontains')
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    quantity__gt = django_filters.NumberFilter(field_name='quantity', lookup_expr='gt')
    quantity__lt = django_filters.NumberFilter(field_name='quantity', lookup_expr='lt')

    class Meta:
        model = Product
        fields = ['availability']