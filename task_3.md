Задание - спроектировать и реализовать на обоих фреймворках структуру и эндпоинты API, определить форматы запросов и ответов, а также обеспечить безопасность и аутентификацию. Представьте, что ваше API будет использоваться как внутри организации, так и внешними клиентами.

Вам необходимо разработать REST API для системы управления задачами (To-Do), который будет обслуживать операции управления задачами и проектами. Ваше API должно обеспечивать следующий функционал:

Управление задачами:
- Создание новой задачи с указанием названия, описания, статуса (выполнена/не выполнена) и срока выполнения и проекта
- Получение списка всех задач.
- Получение информации о конкретной задаче по ее идентификатору.
- Обновление информации о задаче.
- Удаление задачи.

Управление проектами:
- Создание нового проекта с указанием названия и описания.
- Получение списка всех проектов.
- Получение информации о конкретном проекте по его идентификатору.
- Обновление информации о проекте.
- Удаление проекта.
- Получение всех задач проекта.

Связи между задачами и проектами:
- Задачи могут быть связаны с одним или несколькими проектами.


Для выполнения задания может понадобиться

для django:
- [TextChoices](https://docs.djangoproject.com/en/5.0/ref/models/fields/#enumeration-types)
- [ForeignKey](https://docs.djangoproject.com/en/5.0/ref/models/fields/#foreignkey)
- [ForeignKey.related_name](https://docs.djangoproject.com/en/5.0/ref/models/fields/#django.db.models.ForeignKey.related_name)
- [ForeignKey.serializers](https://www.django-rest-framework.org/api-guide/relations/#nested-relationships)

для fast api:
- [relationships](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html)
- [query](https://docs.sqlalchemy.org/en/20/orm/queryguide/)
