import django_filters

from .models import Favorited, ShoppingCart


class RecipeFilter(django_filters.FilterSet):
    author = django_filters.NumberFilter(
        field_name='author__id',
    )
    tags = django_filters.CharFilter(
        field_name='tags__slug', lookup_expr='iexact'
    )
    is_in_shopping_cart = django_filters.NumberFilter(
        method='check_recipes'
    )
    is_favorited = django_filters.NumberFilter(
        method='check_recipes'
    )

    def check_recipes(self, queryset, name, value):
        if self.request.user.is_authenticated:
            if name == 'is_in_shopping_cart':
                filtering_queryset = ShoppingCart.objects.filter(
                    user=self.request.user
                )
                field = 'shopper'
            elif name == 'is_favorited':
                filtering_queryset = Favorited.objects.filter(
                    user=self.request.user
                )
                field = 'fans'
            lookup = '__'.join([field, 'in'])
            if value == 1:
                return queryset.filter(**{lookup: filtering_queryset})
            if value == 0:
                return queryset.exclude(**{lookup: filtering_queryset})
        return queryset
