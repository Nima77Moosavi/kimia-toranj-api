from django_filters import rest_framework as filters
from .models import Product
from django.db.models import Q


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
        # Initialize an empty Q object
        attribute_conditions = Q()

        # Split the attribute filter into key-value pairs
        for pair in value.split(','):
            if ':' in pair:
                key, val = pair.split(':')
                # Add each condition to the Q object using OR logic
                attribute_conditions |= Q(
                    variants__attributes__attribute__name=key,
                    variants__attributes__value=val,
                )

        # Apply the combined conditions to the queryset
        return queryset.filter(attribute_conditions).distinct()
