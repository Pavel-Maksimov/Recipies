from django.contrib.auth.models import AbstractUser
from django.db import models


class FoodgramUser(AbstractUser):
    username = models.CharField('юзернейм',
                                max_length=150,
                                unique=True
                                )
    email = models.EmailField(max_length=254,
                              unique=True
                              )
    first_name = models.CharField('имя',
                                  max_length=150
                                  )
    last_name = models.CharField('фамилия',
                                 max_length=150
                                 )
    password = models.CharField('пароль',
                                max_length=150
                                )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


class Subscription(models.Model):
    subscriber = models.ForeignKey(FoodgramUser, on_delete=models.CASCADE,
                                   related_name='subscribtions')
    author = models.ForeignKey(FoodgramUser, on_delete=models.CASCADE,
                               related_name='subscribers')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        models.UniqueConstraint(
            fields=['subscriber', 'author'],
            name='unique_subscription'
        )

        def __str__(self):
            return f'Пописка {self.subscriber}, автор {self.author}'
