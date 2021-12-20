import django_filters
from .models import *
from dal import autocomplete


class ProductCustomerFilter(django_filters.FilterSet):
    prod_name = django_filters.CharFilter(label='Product name', lookup_expr='icontains')
    #prod_name = django_filters.ModelChoiceFilter(queryset=Product.objects.all(), widget=autocomplete.ModelSelect2)
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    order = django_filters.OrderingFilter(fields=('price','price'))

    class Meta:
        model = Product
        fields = ['prod_name', 'order']



class ProductSearchFilter(django_filters.FilterSet):
    prod_name = django_filters.CharFilter(label='Product name', lookup_expr='icontains')
    #prod_name = django_filters.ModelChoiceFilter(queryset=Product.objects.all(), widget=autocomplete.ModelSelect2)
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    quantity__gt = django_filters.NumberFilter(field_name='quantity', lookup_expr='gt')
    quantity__lt = django_filters.NumberFilter(field_name='quantity', lookup_expr='lt')

    class Meta:
        model = Product
        fields = ['availability', 'prod_name']

