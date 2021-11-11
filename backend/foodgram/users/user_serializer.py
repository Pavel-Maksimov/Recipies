from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from .models import Subscription

User = get_user_model()


class FoodgramUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, author):
        """
        Check if current authenticated user is subscribed to
        requested user.
        """
        if self.context['request'].user.is_authenticated:
            subscription = Subscription.objects.filter(
                author=author,
                subscriber=self.context['request'].user
            )
            if subscription.exists():
                return True
        return False
