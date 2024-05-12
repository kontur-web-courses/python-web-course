from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import declarative_base, mapped_column, Mapped

Base = declarative_base()


class Products(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text())
    price: Mapped[int] = mapped_column(Integer())


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text())
    genre: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer())

    def __str__(self):
        return self.name
