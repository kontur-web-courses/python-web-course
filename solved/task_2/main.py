from fastapi import FastAPI
from models import Products, Book
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


@app.get("/books/")
def get_books():
    books = session.query(Book).all()
    return books


@app.get("/books/{book_id}/")
def get_book(book_id: int):
    book = session.query(Book).filter_by(id=book_id).first()
    return book


@app.post("/books/")
def post_book(name: str, description: str, genre: str, price: int):
    book = Book(name=name, description=description, genre=genre, price=price)
    session.add(book)
    session.commit()
    return {"status": "success"}


@app.put("/books/")
def post_book(book_id: int, name: str, description: str, genre: str, price: int):
    book = session.query(Book).filter_by(id=book_id).first()
    book.name = name
    book.description = description
    book.genre = genre
    book.price = price
    session.commit()
    return {"status": "success"}


@app.delete("/books/")
def delete_book(book_id: int):
    book = session.query(Book).filter_by(id=book_id).first()
    session.delete(book)
    return {"status": "success"}
