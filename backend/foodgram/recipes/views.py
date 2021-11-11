from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .models import Favorited, Ingredient, Recipe, ShoppingCart, Tag
from .pagination import LimitPagePagination
from .permissions import IsAuthorOrStaff
from .serializers import (FavoritedSerializer, IngredientSerializer,
                          RecipeSerializer, ShoppingCartSerializer,
                          TagSerializer)
from .utils import get_shopping_cart


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View to .list() and .retrieve() tags.

    * Available for all users.
    """
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View to .list() and .retrieve() ingredientss.

    * Available for all users.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )


class RecipeViewSet(viewsets.ModelViewSet):
    """
    View to CRUD recipes.

    * Safe methods are available for Anonymous,
    others - for recipe's author or staff only.

    Additional endpoints:
    * 'recipes/favorite/' endpoint allows authenticated user to add and delete
    recipes to favorited list.
    * 'recipes/shopping_cart/' endpoint allows authenticated user to add and
    delete recipes to shopping_cart.
    * 'recipes/download_shopping_cart/' endpoint allows authenticated user to
    download a shopping_cart as .txt file.
    """
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrStaff,
    )
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitPagePagination

    def get_permissions(self):
        if self.action in (
            'favorite',
            'shopping_cart',
            'download_shopping_cart'
        ):
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()

    @action(methods=['get', 'delete'], detail=True)
    def favorite(self, request, *args, **kwargs):
        if request.method == 'GET':
            serializer = FavoritedSerializer(
                data={'id': self.kwargs.get('pk')},
                context={'request': request},
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.method == 'DELETE':
            favorited = get_object_or_404(
                Favorited,
                recipe=self.kwargs.get('pk'),
                user=request.user
            )
            favorited.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get', 'delete'], detail=True)
    def shopping_cart(self, request, *args, **kwargs):
        if request.method == 'GET':
            serializer = ShoppingCartSerializer(
                data={'id': self.kwargs.get('pk')},
                context={'request': request},
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.method == 'DELETE':
            favorited = get_object_or_404(
                ShoppingCart,
                recipe=self.kwargs.get('pk'),
                user=request.user
            )
            favorited.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def download_shopping_cart(self, request):
        sending_data = get_shopping_cart(request)
        return HttpResponse(
            sending_data, headers={
                'Content-Type': 'text/plain',
                'Content-Disposition': ('attachment;'
                                        'filename="shopping_cart.txt"')
            }
        )
