from dataclasses import dataclass
@dataclass
class Book:
    title: str # setting equal to None means its optional to include when constructing
    rating: str
    price: str
