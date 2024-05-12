# Модуль 2. FastAPI
FastAPI - это современный, быстрый и эффективный фреймворк для создания веб-API на языке Python. Он основан на стандарте типов данных Python 3.7+ и использует мощные функции асинхронности, благодаря чему обеспечивает высокую производительность и поддерживает асинхронные операции.
FastAPI является отличным выбором для создания высокопроизводительных и надежных веб-API на Python, обеспечивая простоту использования и богатый набор функций для разработчиков.


## 1. Создать и активировать виртуальное окружение
[инструкция](https://pythonchik.ru/okruzhenie-i-pakety/virtualnoe-okruzhenie-python-venv)


## 2. Подготовка проекта
Сначала установите FastAPI и Uvicorn с помощью pip:
```shell
pip install fastapi uvicorn
```

## 3. Определение модели
Создайте файл с именем models.py в вашем каталоге проекта.
Определение модели продукта: В models.py определите модель Product с необходимыми полями:
```python
from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import declarative_base, mapped_column, Mapped

Base = declarative_base()


class Products(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text())
    price: Mapped[int] = mapped_column(Integer())
```


## 4. Настройка базы данных с Alembic
Установите Alembic для управления миграциями базы данных:
`pip install alembic`

Инициализируйте Alembic в вашем каталоге проекта:
`alembic init alembic`

Отредактируйте файл alembic.ini и настройте URL-адрес вашего соединения с базой данных. Для SQLite это должно выглядеть примерно так:
`sqlalchemy.url = sqlite:///./app.db`

Отредактируйте файл alembic/env.py для настройки миграции:
```python
from models import Base
target_metadata = Base.metadata
```

Создайте первую миграцию с помощью Alembic:
`alembic revision --autogenerate -m "create products table"`

Примените миграции для создания начальной схемы базы данных:
`alembic upgrade head`


## 5. Создание приложения FastAPI
Создайте файл Python с именем main.py в вашем каталоге проекта.
В main.py импортируйте FastAPI и вашу модель Products:
```python
from fastapi import FastAPI
from models import Products
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///./app.db')
Session = sessionmaker(bind=engine)
session = Session()


app = FastAPI()


@app.get("/products/")
def get_products():
    products = session.query(Products).all()
    return products


@app.get("/products/{product_id}/")
def get_product(product_id: int):
    product = session.query(Products).filter_by(id=product_id).first()
    return product


@app.post("/products/")
def post_products(name: str, description: str, price: int):
    product = Products(name=name, description=description, price=price)
    session.add(product)
    session.commit()
    return {"status": "success"}


@app.put("/products/")
def post_product(product_id: int, name: str, description: str, price: int):
    product = session.query(Products).filter_by(id=product_id).first()
    product.name = name
    product.description = description
    product.price = price
    session.commit()
    return {"status": "success"}


@app.delete("/products/")
def delete_product(product_id: int):
    product = session.query(Products).filter_by(id=product_id).first()
    session.delete(product)
    return {"status": "success"}
```


## 6. Запуск приложения FastAPI
Запустите ваше приложение FastAPI с помощью Uvicorn:
`uvicorn main:app --reload`
Протестируйте приложение и возможность просмотра(GET)/создания(POST)/изменения(PUT)/удаления(DELETE)
Это можно сделать на странице автодокументации: http://127.0.0.1:8000/docs/


## 7. Самостоятельная работа
Самостоятельно создать приложение для работы с книгами (просмотр/создание/изменение/удаление).
Модель книг должна содержать имя, описание, автора, жанр и цену.
