from django_filters import rest_framework as filters
from .models import Product


class ProductFilter(filters.FilterSet):
    attribute = filters.CharFilter(method='filter_by_attribute')
    min_price = filters.NumberFilter(
        field_name='variants__price', lookup_expr='gte')  # Price >= min_price
    max_price = filters.NumberFilter(
        field_name='variants__price', lookup_expr='lte')  # Price <= max_price

    class Meta:
        model = Product
        fields = ['attribute', 'min_price', 'max_price']

    def filter_by_attribute(self, queryset, name, value):
        # Split the attribute filter into key-value pairs
        # Example: attribute=Color:Red,Size:Small
        filters = {}
        for pair in value.split(','):
            key, val = pair.split(':')
            filters[f'variants__attributes__attribute__name'] = key
            filters[f'variants__attributes__value'] = val
        return queryset.filter(**filters).distinct()
