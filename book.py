from dataclasses import dataclass
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Numeric
from decimal import Decimal
from config import Base


@dataclass
class Book:
    title: str # setting equal to None means its optional to include when constructing
    rating: str
    price: str



class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(), unique=True)
    rating: Mapped[str] = mapped_column(String())
    price: Mapped[Decimal] = mapped_column(Numeric(10,2))


def to_book_model(book: Book) -> BookModel:
    price = Decimal(book.price[1:])
    bookModel =  BookModel(title = book.title, rating = book.rating, price = price)
    return bookModel

