from urllib.parse import unquote

import django_filters
from rest_framework import filters

from .models import Favorited, ShoppingCart


class RecipeFilter(django_filters.FilterSet):
    """
    Custom filter class for RecipeViewSet.

    Accepted query parameters:
    -'author' - integer, show recipes, that's author has the entered id;
    -'tags' - slug, show recipes with entered tags;
    -'is_in_shopping_cart' - bool, accept valies:
        false - show recipes not included into current user's shopping_cart;
        true - show recipes included into current user's shopping_cart;
    -'is_favorited' - bool, accept valies:
        false - show recipes not included into current user's list
            of favorited recipes;
        true - show recipes included into current user's list
            of favorited recipes;
    """
    author = django_filters.NumberFilter(
        field_name='author__id',
    )
    tags = django_filters.CharFilter(
        field_name='tags__slug', lookup_expr='iexact'
    )
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='check_recipes'
    )
    is_favorited = django_filters.BooleanFilter(
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
            if value is True:
                return queryset.filter(**{lookup: filtering_queryset})
            if value is False:
                return queryset.exclude(**{lookup: filtering_queryset})
        return queryset


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
         field_name='name',
         lookup_expr='icontains',
         method='uncode_url'
    )

    def uncode_url(self, queryset,  name, value):
        return queryset.filter(name__icontains=unquote(value))
