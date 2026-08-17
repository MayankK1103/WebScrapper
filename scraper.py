from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError
from models.book import Book
from models.countries import Country

def retry(base_fn):
    def wrapper_fn(*args, **kwargs):
        error = None
        for i in range(3):
            try:
                html = base_fn(*args, **kwargs)
                return html
            except ConnectionError as e:
                error = e
                print("Retrying")
        if (error):
            raise ConnectionError("Couldn't connect to url server") from error
    return wrapper_fn


class Scraper:

    def __init__(self, url):
        self.url = url
        self.page: requests.models.Response = None

    @retry
    def get(self):
        self.page = requests.get(self.url)
        return self.page

    def soup(self):
        self.parse = BeautifulSoup(self.page.content, "html.parser")    
        return self.parse

    def preprocess(self):
        # design a way to ensure that all the methods are called in the right order
        self.get()
        self.soup()
        return


class BookScraper(Scraper):

    # Inhert parent constructor with additional attributes added
    def __init__(self, url):
        super().__init__(url)
        self.parse = None
        self.books = None
        
    def booksHTML(self):
        self.books = self.parse.find_all("article" , class_ = "product_pod")
        return self.books

    def book_list(self):
        self.book_collection = []
        self.preprocess()

        for book in self.books:
            title = book.h3.a["title"]
            rating = book.find("p", class_ = "star-rating")["class"][-1]
            price = book.find("p", class_ = "price_color").text

            bookObj = Book(title, rating, price)
            self.book_collection.append(bookObj)

        return self.book_collection
    
    def preprocess(self):
        # design a way to ensure that all the methods are called in the right order
        super().preprocess()
        self.booksHTML()
        return

class CountryScraper(Scraper):

    def __init__(self, url):
        super().__init__(url)
        self.parse = None
        self.countries = None

    def countriesHTML(self):
        self.countries = self.parse.find_all("div", class_ = "col-md-4 country")

    def countries_list(self):
        self.countries_collection = []
        self.preprocess()

        for country in self.countries:
            name = country.h3.text.strip()
            capital = country.find("span", class_ = "country-capital").text.strip()
            population = country.find("span", class_ = "country-population").text.strip()
            area = country.find("span", class_ = "country-area").text.strip()

            countryObj = Country(name, capital, population, area)
            self.countries_collection.append(countryObj)

        return self.countries_collection

    def preprocess(self):
        # design a way to ensure that all the methods are called in the right order
        super().preprocess()
        self.countriesHTML()
        return