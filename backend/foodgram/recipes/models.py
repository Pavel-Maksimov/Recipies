from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.deletion import CASCADE

from .colors import COLORS
from .measurement_units import MEASUREMENT_UNIT_CHOICES

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Название тега',
        max_length=200
    )
    color = models.CharField(
        'Цвет в HEX',
        max_length=7,
        default='#49B64E',
        choices=COLORS
    )
    slug = models.SlugField(
        'Уникальный слаг',
        max_length=200,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'Тег {self.slug}'


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингредиента',
        max_length=200
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200,
        choices=MEASUREMENT_UNIT_CHOICES
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'Ингредиент {self.name}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        'Название',
        max_length=200
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/'
    )
    text = models.TextField('Описание')
    cooking_time = models.IntegerField(
        'Время приготовления (в минутах)',
        validators=(
            MinValueValidator(
                limit_value=0,
                message='Время приготовления должно быть больше нуля.'
            ),
        )
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipies',
        verbose_name='Теги'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientContent',
        verbose_name='Ингредиенты'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'Рецепт {self.name}'


class IngredientContent(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='using_ingredients'
    )
    amount = models.PositiveIntegerField('Количество в рецепте')

    class Meta:
        verbose_name = 'Содержание ингредиента в рецепте'
        verbose_name_plural = 'Содержание ингредиентов в рецепте'
        models.UniqueConstraint(
            fields=('using_ingredient', 'recipes'),
            name='once_added_ingredient'
        )

    def __str__(self):
        return (
            f'Содержание ингредиента {self.ingredient}'
            f' в рецепте {self.recipe}'
        )


class Favorited(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='fans'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite'
    )

    class Meta:
        verbose_name = 'Избранные рецепты'
        verbose_name_plural = 'Избранные рецепты'
        models.UniqueConstraint(
            fields=('user', 'recipe'),
            name='once_favorited'
        )


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopper'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sopping_cart'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        models.UniqueConstraint(
            fields=('user', 'recipe'),
            name='once_in_shopping_cart'
        )
