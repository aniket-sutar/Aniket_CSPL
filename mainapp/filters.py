import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    prod_name = django_filters.CharFilter(lookup_expr='icontains')
    price = django_filters.NumberFilter()
    is_active = django_filters.BooleanFilter()
    
    class Meta:
        model = Product
        fields = ['prod_name', 'price', 'is_active']
