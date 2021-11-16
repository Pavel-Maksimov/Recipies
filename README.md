![foodgram_workflow](https://github.com/Pavel-Maksimov/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
# Проект Foodgram
Foodgram - это сервис для публикации рецептов. Авторизованные пользователи могут подписываться на понравившихся авторов, добавлять рецепты в избранное, в покупки, скачать список покупок ингредиентов для добавленных в покупки рецептов.<br>
### Развёртывание проекта <br>
Развёртывание проекта предполагается в контейнере Docker 
(инструкция по установке: https://docs.docker.com/engine/install/). <br>
Для развёртывания проекта выполните следующие действия:<br>
Клонируйте репозиторий:
```
git clone https://github.com/Pavel-Maksimov/foodgram-project-react
```
Находясь в папке infra/, выполните команду:
```
$ docker-compose up -d
```

Создайте и примените миграции:
```
$ docker-compose run web python manage.py makemigrations
$ docker-compose run web python manage.py migrate
```
Для сбора статики выполните команду:
```
$ docker-compose run web python manage.py collectstatic
```
Сервер будет доступен на хосте http://127.0.0.1/. <br>
Для создания суперюзера выполните команду:
```
$ docker-compose exec web python manage.py createsuperuser
```
Для заполнения базы данных начальными данными выполните команду:
```
$ docker exec -it <container_id> python manage.py shell
>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().delete()
>>> quit()

$ docker exec -it <container_id> python manage.py loaddata fixtures.json
```

Для останова сервера выполните команду:
```
$ docker-compose down
```
Имя сервера: ***http://pavelmaksimov.ml/***<br>
Тестовый юзер:<br>
Электронная почта: ivan@mail.ru<br>
Пароль(исправленный): gibbson12345
