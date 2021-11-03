from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .actions import actions
from .models import Favorited, IngredientContent, Tag, Recipe, ShoppingCart
from .serializers import (TagSerializer, RecipeSerializer, FavoritedSerializer,
                          ShoppingCartSerializer)
from .utils import get_shopping_cart


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    @action(methods=['get', 'delete'], detail=True)
    def favorite(self, request, *args, **kwargs):
        if request.method == 'GET':
            serializer = FavoritedSerializer(
                data={'id': self.kwargs.get('pk')},
                context={'request': request},
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            favorited = get_object_or_404(Favorited,
                                          recipe=self.kwargs.get('pk'),
                                          user=request.user)
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
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            favorited = get_object_or_404(ShoppingCart,
                                          recipe=self.kwargs.get('pk'),
                                          user=request.user)
            favorited.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def download_shopping_cart(self, request):
        sending_data = get_shopping_cart(request)
        return HttpResponse(sending_data, headers={
            'Content-Type': 'text/plain',
            'Content-Disposition': 'attachment; filename="shopping_carts.txt"'
        })
