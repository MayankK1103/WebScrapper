from sqlalchemy import text
from scraper import BookScraper
from config import engine

if __name__ == "__main__":
    bs = BookScraper("https://books.toscrape.com/")
    print(bs.book_list())