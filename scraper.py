from bs4 import BeautifulSoup
import requests
from book import Book
from decimal import Decimal



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
            price = Decimal(book.find("p", class_ = "price_color").text[1:])

            bookObj = Book(title, rating, price)
            self.book_collection.append(bookObj)

        return self.book_collection
    
    def preprocess(self):
        # design a way to ensure that all the methods are called in the right order
        self.get()
        self.soup()
        self.booksHTML()
        return

