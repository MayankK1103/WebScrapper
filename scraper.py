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
        if self.page:
            self.parse = BeautifulSoup(self.page.content, "html.parser")
        else:
            self.parse = BeautifulSoup(self.get().content, "html.parser")
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
        # does this also need the if conditional check to see if self.parse already exists
        if self.parse:
            self.books = self.parse.find_all("article" , class_ = "product_pod")
        else:
            self.books = self.soup().find_all("article" , class_ = "product_pod")
        
        return self.books

    def book_list(self):
        self.book_collection = []

        if self.books == None:
            self.booksHTML()

        for book in self.books:
            title = book.h3.a["title"]
            rating = book.find("p", class_ = "star-rating")["class"][-1]
            price = book.find("p", class_ = "price_color").text

            bookObj = Book(title, rating, price)
            self.book_collection.append((bookObj.title, bookObj.rating, bookObj.price))

        return self.book_collection
    
    # Design a run method that does all those manual checks to see if all the 
    # variables are defined and if not call the appropriate methods to do so.
    def run(self):
        pass


bs = BookScraper("https://books.toscrape.com/")
print(bs.book_list())


        
        

        
        
        




# s = Scraper("https://books.toscrape.com/")
# print(s.soup())

books_page = requests.get("https://books.toscrape.com/")
#print(type(books_page))
soup = BeautifulSoup(books_page.content, "html.parser")

books = soup.find_all("article" , class_ = "product_pod")
#print(books)


rating = books[0].find("p", class_ = "star-rating")["class"][-1]
title = books[0].h3.a["title"]
price = books[0].find("p", class_ = "price_color").text

#print(rating, title, price)

book_list = []

for book in books:
    rating = book.find("p", class_ = "star-rating")["class"][-1]
    title = book.h3.a["title"]
    price = book.find("p", class_ = "price_color").text

    book_list.append({"title" : title, "rating" : rating, "price" : price })

#print(book_list)




