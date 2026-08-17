from sqlalchemy.orm import Session
from sqlalchemy import select
from scraper import BookScraper, CountryScraper
from config import engine, Base
from book import BookModel, to_book_model
from countries import CountryModel, to_country_model

# what goes into the pipeline class?
# creating the session engine, the statements, the already exisitng elements
# then the precheck, and then session 

# how to connect the instances of the scrapers to the pipeline class itself
class Pipeline:

    def __init__(self, scraper, scraper_method, to_model_method, db_model, unique): # scraper would be the scraper instance of a type of scraper
        # scraper 
        self.scraper = scraper
        self.scraper_method = scraper_method
        self.to_model_method = to_model_method
        self.db_model = db_model
        self.unique = unique
        self.statement = None
        self.existing = None
        self.instances = None

    def read_db(self):
        with Session(engine) as session:
            self.statement = select(getattr(self.db_model, self.unique))
            self.existing = session.scalars(self.statement).all()
        return self.existing

    def pre_check(self):
        self.instances = []
        method_to_call = getattr(self.scraper, self.scraper_method)

        for item in method_to_call():
            scraped_data = getattr(item, self.unique)
            if scraped_data not in self.existing:
                self.instances.append(self.to_model_method(item))

    def add_db(self):
        self.preprocess()
        with Session(engine) as session:
            session.add_all(self.instances)
            session.commit()

    def preprocess(self):
        self.read_db()
        self.pre_check()
        return

        


if __name__ == "__main__":
    Base.metadata.create_all(engine) # don't need after initial setup as this establishes
    # the one time connection
    
    book_pipeline = Pipeline(
        BookScraper("https://books.toscrape.com/"), 
        "book_list", 
        to_book_model, 
        BookModel, 
        "title"
        )
    book_pipeline.add_db()

    country_pipeline = Pipeline(
        CountryScraper("https://scrapethissite.com/pages/simple/"),
        "countries_list",
        to_country_model,
        CountryModel,
        "name"
    )
    country_pipeline.add_db()
    
    
   

    
