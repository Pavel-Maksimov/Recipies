from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer

from .models import Subscription
from rest_framework import serializers

User = get_user_model()


class RecipesSerializer(serializers.ModelSerializer):
    pass


class FoodgramUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "password",)


class FoodgramUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("email", 'id', "username", "first_name",
                  "last_name", 'is_subscribed')

    def get_is_subscribed(self, author):
        subscription = Subscription.objects.filter(
            author=author,
            subscriber=self.context['request'].user
        )
        if subscription.exists():
            return True
        return False


class AuthorSerializer(FoodgramUserSerializer):
    recipes = RecipesSerializer(many=True,
                                required=False)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("email", 'id', "username", "first_name",
                  "last_name", 'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, recipes):
        pass


class AuthorField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        author = User.objects.get(id=value.pk)
        serializer = AuthorSerializer(
            author, context={'request': self.context['request']})
        return serializer.data


class SubscriptionSerializer(serializers.ModelSerializer):
    author = AuthorField(
        queryset=User.objects.all()
    )
    subscriber = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True
    )

    class Meta:
        model = Subscription
        fields = ('author', 'subscriber')

    def create(self, validated_data):
        return Subscription.objects.create(
            author=validated_data['author'],
            subscriber=validated_data['subscriber']
        )
