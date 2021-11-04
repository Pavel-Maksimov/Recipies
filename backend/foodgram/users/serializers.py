from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Recipe

from recipes.serializers import RecipeSerializer
from .models import Subscription
from rest_framework import serializers
from .user_serializer import FoodgramUserSerializer

User = get_user_model()


class FoodgramUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "password",)


# class FoodgramUserSerializer(UserSerializer):
#     is_subscribed = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = ("email", 'id', "username", "first_name",
#                   "last_name", 'is_subscribed')

#     def get_is_subscribed(self, author):
#         subscription = Subscription.objects.filter(
#             author=author,
#             subscriber=self.context['request'].user
#         )
#         if subscription.exists():
#             return True
#         return False


class ShortRecipeSerializer(RecipeSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class AuthorSerializer(FoodgramUserSerializer):
    recipes = ShortRecipeSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("email", 'id', "username", "first_name",
                  "last_name", 'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            recipes_limit = abs(int(
                self.context['request'].query_params['recipes_limit']
            ))
        except (KeyError, ValueError):
            recipes_limit = None
        representation['recipes'] = representation['recipes'][:recipes_limit]
        return representation


class AuthorField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        author = User.objects.get(id=value.pk)
        serializer = AuthorSerializer(
            author, context={'request': self.context['request']})
        return serializer.data


class SubscriptionSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True
    )
    subscriber = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True
    )

    class Meta:
        model = Subscription
        fields = ('author', 'subscriber')

    # def create(self, validated_data):
    #     print('val.data:', validated_data)
    #     return Subscription.objects.create(
    #         author=validated_data['author'],
    #         subscriber=validated_data['subscriber']
        # )

    def to_representation(self, value):
        author = User.objects.get(id=value.author.id)
        serializer = AuthorSerializer(
            author, context={'request': self.context['request']})
        return serializer.data
