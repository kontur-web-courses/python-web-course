# Практический курс по построению Web API на python

## Подготовка в работе
1. Клонировать репозиторий `https://github.com/kontur-web-courses/python-web-course`
2. Развернуть виртуальное окружение и установить зависимости из `requirements.txt`. 
C помощью IDE (например PyCharm) или командной строки:  
```shell
$ python3 -m venv venv # создание виртуального окрущения

$ venv\Scripts\activate.bat # активация виртуального окружения для Windows
$ source venv/bin/activate # активация виртуального окружения для Linux и MacOS

(venv)$ pip3 install -r requirements.txt # установка зависимостей

(venv)$ deactivate # выход из виртуального окружения, после завершения работы над проектом
```


## Генерация тестовых данных
Для регенерации тестовых данных можно зайти в админку под суперпользователем и на
вкладке "Ключи" нажать "Перегенерировать все данные" выполнится функция ```srvices.data.
regenerate()``` после ее
выполнения БД будет очищена и наполнена тестовыми данными, будет создано три
организации и 19 сотрудников. В каждой из организаций будет добавлено по 4 сотрудника
1 админ, 2 пользователя и 1 утверждающий(approver). Остальные сотрудники останутся 
без привязки к организации, трое из них будет с флагом ```deleted=True``` 
Каждая роль(Roles) имеет свои операции(Operations)
Также будет перегенерирован ключ для доступа к апи, он будет годен 24 часа, при 
запросах в апи его необходимо включать в заголовки ```headers={"Token": api_token}```


## Вспомогательные инструменты

### Линтер

flake8 - инструмент, позволяющий просканировать код проекта и обнаружить в нем 
стилистические ошибки.\
Запустить можно (в корне проекта): ```flake8 .```\
Конфигурируется в файле ```.flake8``` в корне проекта

Документация - https://flake8.pycqa.org/en/latest/

### Анализатор типов

mypy - это средство проверки статических типов для Python.
Запустить можно (в корне проекта): ```mypy .```\
Конфигурируется в файле ```mypy.ini``` в корне проекта

Документация - https://mypy.readthedocs.io/en/stable/

### Тестирование

pytest - это среда тестирования, основанная на Python.
Запустить можно (в корне проекта): ```pytest .```\
Конфигурируется в файле ```pytest.ini``` в корне проекта

Документация - https://pytest-docs-ru.readthedocs.io/ru/latest/


## Модели

### Organization - организации

- В организации можно добавлять несколько сотрудников, только с флагом 
  ```deleted=False```
- У организации есть реквизиты Requisites

### Requisites - реквизиты организации

- Реквизиты привязываются к организации и выбираются из списка RequisitesName

### Employee - сотрудники

- Сотрудники это User с флагом ```is_superuser = False```
- Сотрудник может быть помечен как удаленный ```deleted=False```
- У сотрудника назначаются в организации определенные роли(RoleOperations)

### RoleOperations - операции для роли

- Список операции(Operations) привязанных к роли(Roles)


## АПИ

Для работы с апи необходимо использовать апи-ключ, он генерируется и доступен в админке

### Сотрудники
- Получение списка сотрудников
- Получение одного сотрудника по portal_user_id
- Создание сотрудника
- Обновление сотрудника

### Организации
- Получение списка организаций
- Получение одной организации по id
- Создание организации
- Обновление организации
- Добавление сотрудника в организацию