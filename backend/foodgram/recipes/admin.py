from django.conf import settings
from django.contrib import admin

from .models import (Favorited, Ingredient, IngredientContent, Recipe,
                     ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    search_fields = ('id', 'name', 'color', 'slug',)
    empty_value_display = settings.ADMIN_EMPTY_VALUE


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    list_filter = ('name',)
    empty_value_display = settings.ADMIN_EMPTY_VALUE


@admin.register(IngredientContent)
class IngredientContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount',)
    list_filter = ('recipe', 'ingredient',)
    empty_value_display = settings.ADMIN_EMPTY_VALUE


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'text',
                    'cooking_time',)
    list_filter = ('author', 'name', 'tags',)
    empty_value_display = settings.ADMIN_EMPTY_VALUE


@admin.register(Favorited, ShoppingCart)
class FavoritedAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user',)
    search_fields = ('id', 'recipe', 'user',)
    empty_value_display = settings.ADMIN_EMPTY_VALUE
