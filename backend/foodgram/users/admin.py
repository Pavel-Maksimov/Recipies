from django.contrib import admin

from .models import Subscription, FoodgramUser


@admin.register(FoodgramUser)
class FoodgramUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "email", "is_staff",)
    list_filter = ("email", "username",)
    empty_value_display = "-пусто-"


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "subscriber", "author",)
    search_fields = ("subscriber", "author",)
    empty_value_display = "-пусто-"
