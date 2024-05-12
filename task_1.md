# Модуль 1. Django + Django REST Framework (DRF)
Django — это фреймворк, то есть набор готовых инструментов и функций. С его помощью можно быстрее и проще реализовывать на Python сайты и приложения, которые работают в браузере.
С помощью Django framework можно очень быстро, как из конструктора, настроить и запустить работающий веб-сервис — а потом программировать только специфичные функции и бизнес-логику.
Подробнее почитать про django:
- [официальный сайт (на английском)](https://www.djangoproject.com/)
- [перевод документации](https://django.fun/docs/django/5.0/)

Django REST Framework (DRF) — это мощный инструмент для создания веб-API на основе Django, популярного фреймворка для веб-приложений на Python. DRF обеспечивает простоту и гибкость в разработке API, предоставляя инструменты для сериализации данных, авторизации, аутентификации, разрешения доступа и многое другое. Благодаря своей интеграции с Django, DRF упрощает создание RESTful API, позволяя разработчикам сосредоточиться на бизнес-логике приложения.
Подробнее почитать про DRF:
- [официальный сайт](https://www.django-rest-framework.org/)
- [документация на русском](https://github.com/ilyachch/django-rest-framework-rusdoc)

## 1. Создать и активировать виртуальное окружение
[инструкция](https://pythonchik.ru/okruzhenie-i-pakety/virtualnoe-okruzhenie-python-venv)

## 2. Установить django 
`pip install django`

## 3. Создать новый проект 
`django-admin startproject app .`

## 4. Выполнить миграции
`python manage.py migrate`
Миграции в Django - это механизм, который позволяет автоматически изменять структуру базы данных в соответствии с изменениями моделей Django. Когда вы создаете новую модель или вносите изменения в существующую, Django может сгенерировать миграцию, которая описывает необходимые изменения в базе данных. После того как миграция создана, вы можете применить её к базе данных, что приведет к применению этих изменений к реальной базе данных.
Миграции важны для обеспечения целостности и согласованности базы данных с вашими моделями. Они позволяют вам эффективно управлять изменениями в структуре данных без необходимости ручного вмешательства в базу данных. Первоначальное создание миграций необходимо, чтобы начать отслеживать изменения в вашей базе данных с момента создания моделей. Это позволяет вам легко воспроизвести структуру базы данных на других серверах или участках разработки, а также делать откат изменений в случае необходимости.
В качестве БД в этом курсе мы будем использовать стандартную [SQLite](https://www.sqlite.org/).

## 5. Запустить проект
`python manage.py runserver`
Перейти по адресу http://127.0.0.1:8000/ и убедиться что проект запущен (должна открыться стартовая страница django)

## 6. Установить DRF
`pip install djangorestframework`

## 7. Настроить DRF
Добавьте DRF в INSTALLED_APPS: Откройте файл app/settings.py вашего проекта Django и добавьте 'rest_framework' в список INSTALLED_APPS:
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```


## 8. Создадим приложение products
`python manage.py startapp products`


## 9. Подключим приложение products
Откройте файл app/settings.py вашего проекта Django и добавьте 'products' в список INSTALLED_APPS:
```python
INSTALLED_APPS = [
    ...
    "products",
]
```

## 10. Создадим модель данных
В файл products/models.py добавить модель данных: 
```python
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()

    def __str__(self):
        return self.name
```

## 11. Создадим и произведём миграции для формирования схемы в БД
`python manage.py makemigrations`
`python manage.py migrate`

## 12. Создание сериализатора
Сериализаторы (serializers) в Django REST Framework (DRF) играют ключевую роль в преобразовании сложных типов данных, таких как объекты моделей Django, в форматы, подходящие для передачи через API (например, JSON). Они также обрабатывают валидацию входных данных и обратное преобразование данных из формата запроса в объекты Python.

Определите сериализатор Django REST framework в файле products/serializers.py (нужно создать):

```python
from rest_framework import serializers
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price']
```

## 13. Создание представления
Представления (views) в Django REST Framework (DRF) отвечают за обработку HTTP-запросов и формирование HTTP-ответов. Они определяют логику обработки запросов, включая сериализацию и валидацию данных, а также формирование ответов.

Определите представление Django REST framework в файле products/views.py:

```python
from products.models import Product
from products.serializers import ProductSerializer
from rest_framework import viewsets


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

## 14. Создание маршрутов
Маршруты определяют URL-адреса, которые соответствуют определённым действиям в вашем API. Они обычно соотносятся с представлениями (views), которые обрабатывают запросы к этим URL-адресам

Определите маршруты Django REST framework в файле app/urls.py вашего приложения:

```python
from django.contrib import admin
from django.urls import path, include
from products.views import ProductViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("admin/", admin.site.urls),
]
```

## 15. Запуск и проверка API
Запустить проект `python manage.py runserver`
Перейти по адресу `http://127.0.0.1:8000/products/` и протестировать просмотр/создание/изменение/удаление продуктов

## 16. Подключение панели администратора
В django есть встроенная панель администратора доступная по адресу: http://127.0.0.1:8000/admin/

## 17. Создание суперпользователя
Для входа в админку нужно создать пользователя:
`python manage.py createsuperuser`

## 18. Подключение своей модели к админке
Зарегистрировать свою модель в админке с нужными полями, в файле products/admin.py:

```python
from django.contrib import admin
from products.models import Product


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "price")
```

## 19. Проверить модель в панели администратора
Зайти по адресу http://127.0.0.1:8000/admin/
Проверить наличие модели products, попробовать создать/изменить/удалить запись


## 20. Самостоятельная работа
Самостоятельно создать приложение для работы с книгами (просмотр/создание/изменение/удаление).
Модель книг должна содержать имя, описание, автора, жанр и цену.
