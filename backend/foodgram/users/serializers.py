from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from rest_framework import serializers

from .models import Subscription
from .user_serializer import FoodgramUserSerializer

User = get_user_model()


class FoodgramUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password',)


class ShortRecipeSerializer(RecipeSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class AuthorSerializer(FoodgramUserSerializer):
    recipes = ShortRecipeSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'recipes', 'recipes_count'
        )

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
            author, context={'request': self.context['request']}
        )
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

    def to_representation(self, value):
        author = User.objects.get(id=value.author.id)
        serializer = AuthorSerializer(
            author, context={'request': self.context['request']})
        return serializer.data

    def validate(self, data):
        """
        Check if the user is requested to subscribe on
        is not current user and is not already in subscriptions.
        """
        if data['author'] == data['subscriber']:
            raise serializers.ValidationError(
                'Вы не можете подписаться на самого себя.'
            )
        subscription = Subscription.objects.filter(
            author=data['author'],
            subscriber=data['subscriber']
        )
        if subscription.exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого автора.'
            )
        return data
