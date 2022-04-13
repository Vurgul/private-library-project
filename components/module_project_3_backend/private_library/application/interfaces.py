from abc import ABC, abstractmethod
from typing import Optional, List

from .dataclasses import User, Book, Journal


class UsersRepo(ABC):

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[User]: ...

    @abstractmethod
    def add(self, user: User): ...

    @abstractmethod
    def remove(self, user: User): ...

    @abstractmethod
    def get_all(self) -> List[User]: ...

    @abstractmethod
    def get_by_user_data(self, login: str, password: str) -> User: ...

    @abstractmethod
    def get_by_login(self, login: str) -> Optional[User]: ...


class BooksRepo(ABC):

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Book]: ...

    @abstractmethod
    def add(self, book: Book): ...

    @abstractmethod
    def remove(self, book: Book): ...

    @abstractmethod
    def get_all(self) -> List[Book]: ...

    @abstractmethod
    def get_by_isbn13(self, isbn13: str) -> Optional[Book]: ...

    @abstractmethod
    def filter_by_keyword(
        self,
        keyword: str,
        value
    ) -> List[Book]: ...

    @abstractmethod
    def filter_by_price(self, price: float, books: List[Book]) -> List[Book]: ...

    @abstractmethod
    def filter_by_authors(self, price: float, books: List[Book]) -> List[Book]: ...

    @abstractmethod
    def order_by_keyword(self, keyword) -> List[Book]: ...


class JournalRepo(ABC):

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Journal]: ...

    @abstractmethod
    def add(self, journal: Journal): ...

    @abstractmethod
    def remove(self, journal: Journal): ...

    @abstractmethod
    def get_all(self) -> List[Journal]: ...

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[Journal]: ...

    @abstractmethod
    def get_by_book_id(self, book_id: int) -> List[Journal]: ...

    @abstractmethod
    def get_active_record(self, user_id: int) -> Optional[Journal]: ...
