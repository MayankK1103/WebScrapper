from dataclasses import dataclass
from bs4 import BeautifulSoup
import requests

class Scraper:

    def __init__(self, url):
        self.url = url
        self.page: requests.models.Response = None

    def get(self):
        self.page = requests.get(self.url)
        return self.page
    def soup(self):
        self.parse = BeautifulSoup(self.page.content, "html.parser")    
        return self.parse

@dataclass
class Book:
    title: str # setting equal to None means its optional to include when constructing
    rating: str
    price: str

class BookScraper(Scraper):

    # Inhert the same constructor, maybe not if need to add other attributes that need
    # default values assigned when object is created
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
    
    # Design a run method that does all those manual checks to see if all the 
    # variables are defined and if not call the appropriate methods to do so.
    def preprocess(self):
        # design a way to ensure that all the methods are called in the right order
        self.get()
        self.soup()
        self.booksHTML()
        return

bs = BookScraper("https://books.toscrape.com/")
print(bs.book_list())