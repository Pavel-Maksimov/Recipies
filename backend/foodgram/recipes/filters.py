import django_filters

from .models import Favorited, ShoppingCart


class RecipeFilter(django_filters.FilterSet):
    """
    Custom filter class for RecipeViewSet.

    Accepted query parameters:
    -'author' - integer, show recipes, that's author has the entered id;
    -'tags' - slug, show recipes with entered tags;
    -'is_in_shopping_cart' - integer, accept valies:
        0 - show recipes not included into current user's shopping_cart;
        1 - show recipes included into current user's shopping_cart;
    -'is_favorited' - integer, accept valies:
        0 - show recipes not included into current user's list
            of favorited recipes;
        1 - show recipes included into current user's list
            of favorited recipes;
    """
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
