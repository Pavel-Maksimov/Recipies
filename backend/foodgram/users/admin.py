from django.conf import settings
from django.contrib import admin

from .models import FoodgramUser, Subscription


@admin.register(FoodgramUser)
class FoodgramUserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'first_name',
        'last_name', 'email', 'is_staff',
    )
    list_filter = ('email', 'username',)
    empty_value_display = settings.ADMIN_EMPTY_VALUE


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'subscriber', 'author',)
    search_fields = ('subscriber', 'author',)
    empty_value_display = settings.ADMIN_EMPTY_VALUE
