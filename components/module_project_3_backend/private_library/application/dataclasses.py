from datetime import datetime, timedelta
from typing import Optional

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
    tag: str
    subtitle: Optional[str] = None
    desc: Optional[str] = None
    id: Optional[int] = None


@attr.dataclass
class Journal:
    user_id: int
    book_id: int
    status: str
    timedelta: Optional[timedelta] = None
    taking_date: Optional[datetime] = None
    returning_date: Optional[datetime] = None
    id: Optional[int] = None
