from scraper import *
from config import *

bs = BookScraper("https://books.toscrape.com/")
print(bs.book_list())