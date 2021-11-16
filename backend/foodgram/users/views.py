from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from recipes.pagination import LimitPagePagination

from .models import Subscription
from .serializers import SubscriptionSerializer

User = get_user_model()


class FoodgramUserViewSet(UserViewSet):
    """
    View to manage users/ endpoints.

    * Allow read data for Anonymous users,
    others - for authenticated users or staff only.

    Additional endpoints:
    * 'users/subscribe/' endpoint allows authenticated user to subscribe
    and unsubscribe to other users.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = LimitPagePagination

    def get_permissions(self):
        if self.action == 'subscribe':
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()

    @action(methods=['get', 'delete'], detail=True)
    def subscribe(self, request, *args, **kwargs):
        if request.method == 'GET':
            serializer = SubscriptionSerializer(
                data={
                    'author': self.kwargs.get('id'),
                    'subscriber': request.user.id
                },
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
            author = get_object_or_404(User, id=self.kwargs.get('id'))
            subscriber = get_object_or_404(User, id=request.user.id)
            subscriptions = Subscription.objects.filter(
                author=author,
                subscriber=subscriber
            )
            for subscription in subscriptions:
                subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsAPIView(ListAPIView):
    """
    View allows for authenticated users to get a list of subscribtions
    to other users.
    """
    serializer_class = SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = LimitPagePagination

    def get_queryset(self):
        return Subscription.objects.filter(subscriber=self.request.user.id)
