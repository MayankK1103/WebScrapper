from sqlalchemy.orm import Session
from sqlalchemy import select
from scraper import BookScraper
from config import engine
from book import Base, to_model, BookModel

if __name__ == "__main__":
    # Base.metadata.create_all(engine) don't need after initial setup as this establishes
    # the one time connection
    bs = BookScraper("https://books.toscrape.com/")

    with Session(engine) as session:
        statement = select(BookModel.title)
        existing_books = session.scalars(statement).all()

    model_instances = []
    for item in bs.book_list():
        if item.title not in existing_books:
            model_instances.append(to_model(item))

    with Session(engine) as session:
        session.add_all(model_instances)
        session.commit()

    
