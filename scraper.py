from bs4 import BeautifulSoup
import requests

books_page = requests.get("https://books.toscrape.com/")
soup = BeautifulSoup(books_page.content, "html.parser")

books = soup.find_all("article" , class_ = "product_pod")


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

print(book_list)




