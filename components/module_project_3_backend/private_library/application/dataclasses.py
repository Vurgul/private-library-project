from typing import Optional
from datetime import datetime
import attr


@attr.dataclass
class User:
    name: str
    login: str
    password: str
    age: Optional[int] = None
    id: Optional[int] = None


@attr.dataclass
class Book:
    title: str
    authors: str
    publisher: str
    language: str
    isbn13: str
    pages: int
    year: int
    rating: float
    price_USD: float
    desc: Optional[str] = None
    id: Optional[int] = None


@attr.dataclass
class Journal:
    user_id: int
    book_id: int
    action: str
    id: Optional[int] = None
    taking_date: Optional[datetime] = None
    returning_date: Optional[datetime] = None
