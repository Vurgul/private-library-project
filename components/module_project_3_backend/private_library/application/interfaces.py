from abc import ABC, abstractmethod
from typing import List, Optional

from .dataclasses import Book, Journal, User


class UsersRepo(ABC):

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[User]:
        ...

    @abstractmethod
    def add(self, user: User):
        ...

    @abstractmethod
    def get_all(self) -> List[User]:
        ...

    @abstractmethod
    def get_by_user_data(self, login: str, password: str) -> User:
        ...

    @abstractmethod
    def get_by_login(self, login: str) -> Optional[User]:
        ...


class BooksRepo(ABC):

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Book]:
        ...

    @abstractmethod
    def add(self, book: Book):
        ...

    @abstractmethod
    def get_all(self) -> List[Book]:
        ...

    @abstractmethod
    def get_by_isbn13(self, isbn13: str) -> Optional[Book]:
        ...

    @abstractmethod
    def filter_by_price(self, price: str, query):
        ...

    @abstractmethod
    def filter_by_authors(self, authors: str, query):
        ...

    @abstractmethod
    def filter_by_keyword(self, publisher: str, query):
        ...

    @abstractmethod
    def filter_by_publisher(self, publisher: str, query):
        ...

    @abstractmethod
    def order_by(self, column: str, query):
        ...

    @abstractmethod
    def get_top_three(self, tag: str) -> List[Book]:
        ...

    @abstractmethod
    def get_query(self):
        ...

    @abstractmethod
    def get_filter_data(self, query) -> List[Book]:
        ...


class JournalRepo(ABC):

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Journal]:
        ...

    @abstractmethod
    def add(self, journal: Journal):
        ...

    @abstractmethod
    def get_all(self) -> List[Journal]:
        ...

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[Journal]:
        ...

    @abstractmethod
    def get_by_book_id(self, book_id: int) -> List[Journal]:
        ...

    @abstractmethod
    def get_active_record(self, user_id: int) -> Optional[Journal]:
        ...
