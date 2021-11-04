from drf_base64.fields import Base64ImageField
from django.conf import settings
from django.core.files.images import ImageFile
from django.utils import http
from rest_framework import serializers

from . import models as m
from users.user_serializer import FoodgramUserSerializer


class CustomImageFiled(Base64ImageField):
    def to_representation(self, value):
        return value.url

    # def to_internal_value(self, data):
    #     # print('data', data)
    #     data = http.urlsafe_base64_decode(data)
    #     path = settings.MEDIA_ROOT + f'/{self.field_name}.jpeg'
    #     print('self.field_name:', self.field_name)
    #     f = open(path, 'wb')
    #     # print('data', data)
    #     f.write(data)
    #     f.close()
    #     # print('data', data)
    #     print('ImageFile(f).name:', ImageFile(f).name)
    #     return ImageFile(f).name


class TagField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        serializer = TagSerializer(value)
        return serializer.data

    def to_internal_value(self, data):
        return data


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientContentSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=m.Ingredient.objects.all(),
        source='ingredient.id'
    )
    name = serializers.CharField(source='ingredient.name',
                                 read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )
    amount = serializers.IntegerField()

    class Meta:
        model = m.IngredientContent
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientContentSerializer(many=True)
    tags = TagField(
        many=True,
        queryset=m.Tag.objects.all()
    )
    author = FoodgramUserSerializer(
        read_only=True, default=serializers.CurrentUserDefault())
    image = CustomImageFiled()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = m.Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, obj):
        favorited = m.Favorited.objects.filter(
            recipe=obj,
            user=self.context['request'].user
        )
        if favorited.exists():
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        shopping_cart = m.ShoppingCart.objects.filter(
            recipe=obj,
            user=self.context['request'].user
        )
        if shopping_cart.exists():
            return True
        return False

    def create(self, validated_data):
        print('self.context[request]:', self.context)
        new_recipe = m.Recipe.objects.create(
            author=self.context['request'].user,
            image=validated_data['image'],
            name=validated_data['name'],
            text=validated_data['text'],
            cooking_time=validated_data['cooking_time'],
        )
        ingredients = validated_data['ingredients']
        for ingredient in ingredients:
            ingr, amount = ingredient.values()
            m.IngredientContent.objects.create(
                recipe=new_recipe,
                ingredient=ingr['id'],
                amount=amount
            )
        new_recipe.tags.set(validated_data['tags'])
        return new_recipe


class FavoritedSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=m.Recipe.objects.all(),
                                            source='recipe.id')
    name = serializers.CharField(source='recipe.name',
                                 read_only=True)
    image = serializers.ImageField(source='recipe.image',
                                   read_only=True)
    cooking_time = serializers.IntegerField(source='recipe.cooking_time',
                                            read_only=True)

    class Meta:
        model = m.Favorited
        fields = ('id', 'name', 'image', 'cooking_time')

    def create(self, validated_data):
        print('validated_data', validated_data)
        return m.Favorited.objects.create(
            recipe=validated_data['recipe']['id'],
            user=self.context['request'].user
        )


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=m.Recipe.objects.all(),
                                            source='recipe.id')
    name = serializers.CharField(source='recipe.name',
                                 read_only=True)
    image = serializers.ImageField(source='recipe.image',
                                   read_only=True)
    cooking_time = serializers.IntegerField(source='recipe.cooking_time',
                                            read_only=True)

    class Meta:
        model = m.Favorited
        fields = ('id', 'name', 'image', 'cooking_time')

    def create(self, validated_data):
        print('validated_data', validated_data)
        return m.ShoppingCart.objects.create(
            recipe=validated_data['recipe']['id'],
            user=self.context['request'].user
        )
