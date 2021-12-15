import django_filters
from .models import *

class OrderSearchFilter(django_filters.FilterSet):
    customer__name = django_filters.CharFilter(label='Customer name', lookup_expr='icontains')
    customer__email = django_filters.CharFilter(label='Customer email', lookup_expr='icontains')
    class Meta:
        model = Order
        fields = ['status']