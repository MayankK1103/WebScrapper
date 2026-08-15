from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import select
from book import BookModel
from pydantic import BaseModel
from config import engine
from decimal import Decimal

app = FastAPI()

# Pydantic Schema

class BookOut(BaseModel):
    title: str
    rating : str
    price : Decimal
    # permission to read the attributes from the data returned from database
    model_config = {"from_attributes": True}


# get is to retrieve data from the db and send out
@app.get("/books", response_model = list[BookOut])
def get_books():

    with Session(engine) as session:
        statement = select(BookModel)
        existing_books = session.scalars(statement).all()

    return existing_books