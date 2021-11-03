from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()

router_v1.register('users',
                   views.FoodgramUserViewSet)

urlpatterns = [
    path('users/subscriptions/',
         views.SubscriptionsAPIView.as_view(),
         name='subscriptions'),
    path('', include(router_v1.urls)),
]
