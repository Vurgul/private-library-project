from typing import Optional, List

from evraz.classic.components import component
from evraz.classic.sql_storage import BaseRepository
from sqlalchemy import select
from private_library.application import interfaces
from private_library.application.dataclasses import User, Book, Journal


@component
class UsersRepo(BaseRepository, interfaces.UsersRepo):

    def get_by_id(self, id: int) -> Optional[User]:
        query = select(User).where(User.id == id)
        return self.session.execute(query).scalars().one_or_none()

    def add(self, user: User):
        self.session.add(user)
        self.session.flush()

    def get_all(self) -> List[User]:
        query = select(User)
        return self.session.execute(query).scalars().all()

    def remove(self, user: User):
        self.session.delete(user)

    def get_by_user_data(self, login: str, password: str) -> Optional[User]:
        query = select(User).where(
            User.login == login,
            User.password == password,
        )
        return self.session.execute(query).scalars().one_or_none()

    def get_by_login(self, login: str) -> Optional[User]:
        query = select(User).where(User.login == login)
        return self.session.execute(query).scalars().one_or_none()


@component
class BooksRepo(BaseRepository, interfaces.BooksRepo):

    def get_by_id(self, id: int) -> Optional[Book]:
        query = select(Book).where(Book.id == id)
        return self.session.execute(query).scalars().one_or_none()

    def add(self, book: Book):
        self.session.add(book)
        self.session.flush()

    def remove(self, book: Book):
        self.session.delete(book)

    def get_all(self) -> List[Book]:
        query = select(Book)
        return self.session.execute(query).scalars().all()

    def get_by_isbn13(self, isbn13: str) -> Optional[Book]:
        query = select(Book).where(Book.isbn13 == isbn13)
        return self.session.execute(query).scalars().one_or_none()

    def filter_by_keyword(
        self,
        keyword: str,
        value
    ) -> List[Book]:
        if keyword == 'price_USD':
            query = select(Book).where(Book.price_USD == value)
            return self.session.execute(query).scalars().all()
        if keyword == 'authors':
            query = select(Book).where(Book.authors == value)
            return self.session.execute(query).scalars().all()
        if keyword == 'publisher':
            query = select(Book).where(Book.publisher == value)
            return self.session.execute(query).scalars().all()

    def filter_by_price(self, price: float, books: List[Book]) -> List[Book]:
        query = select(Book).where(
            Book.price_USD == price,
            Book in books
        )
        return self.session.execute(query).scalars().all()

    def filter_by_authors(self, price: float, books: List[Book]) -> List[Book]:
        query = select(Book).where(
            Book.price_USD == price,
            Book in books
        )
        return self.session.execute(query).scalars().all()

    def order_by_keyword(self, keyword) -> List[Book]:
        if keyword == 'price_USD':
            query = (
                select(Book).order_by(Book.price_USD)
            )
            return self.session.execute(query).scalars().all()
        if keyword == 'pages':
            query = (
                select(Book).order_by(Book.pages)
            )
            return self.session.execute(query).scalars().all()
        self.get_all()


@component
class JournalRepo(BooksRepo, interfaces.JournalRepo):

    def get_by_id(self, id: int) -> Optional[Journal]:
        query = select(Journal).where(Journal.id == id)
        return self.session.execute(query).scalars().one_or_none()

    def add(self, journal: Journal):
        self.session.add(journal)
        self.session.flush()

    def remove(self, journal: Journal):
        self.session.delete(journal)

    def get_all(self) -> List[Journal]:
        query = select(Journal)
        return self.session.execute(query).scalars().all()

    def get_by_user_id(self, user_id: int) -> List[Journal]:
        query = select(Journal).where(Journal.user_id == user_id)
        return self.session.execute(query).scalars().all()

    def get_by_book_id(self, book_id: int) -> List[Journal]:
        query = select(Journal).where(Journal.book_id == book_id)
        return self.session.execute(query).scalars().all()

    def get_active_record(self, user_id: int) -> Optional[Journal]:
        query = select(Journal).where(
            Journal.action == 'take',
            Journal.user_id == user_id
        )
        return self.session.execute(query).scalars().one_or_none()
