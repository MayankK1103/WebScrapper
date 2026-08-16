from dataclasses import dataclass
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from config import Base


@dataclass
class Country:
    name: str
    capital: str
    population: str
    area: str


class CountryModel(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    capital: Mapped[str] = mapped_column()
    population: Mapped[int] = mapped_column()
    area: Mapped[float] = mapped_column()

def to_country_model(country: Country) -> CountryModel:
    population = int(country.population)
    area = float(country.area)
    countryModel = CountryModel(name = country.name, capital = country.capital, population = population, area = area)
    return countryModel