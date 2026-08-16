from sqlalchemy.orm import Session
from sqlalchemy import select
from scraper import BookScraper, CountryScraper
from config import engine, Base
from book import BookModel, to_book_model
from countries import CountryModel, to_country_model

if __name__ == "__main__":
    Base.metadata.create_all(engine) #don't need after initial setup as this establishes
    # the one time connection
    bs = BookScraper("https://books.toscrape.com/")
    cs = CountryScraper("https://scrapethissite.com/pages/simple/")


    with Session(engine) as session:
        book_statement = select(BookModel.title)
        country_statement = select(CountryModel.name)

        existing_books = session.scalars(book_statement).all()
        existing_countries = session.scalars(country_statement).all()

    book_model_instances = []
    for item in bs.book_list():
        if item.title not in existing_books:
            book_model_instances.append(to_book_model(item))

    country_model_instances = []
    for item in cs.countries_list():
        if item.name not in existing_countries:
            country_model_instances.append(to_country_model(item))


    with Session(engine) as session:
        session.add_all(book_model_instances)
        session.add_all(country_model_instances)
        session.commit()

    
