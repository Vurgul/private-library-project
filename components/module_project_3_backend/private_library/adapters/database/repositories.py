from datetime import datetime
from typing import List, Optional

from evraz.classic.components import component
from evraz.classic.sql_storage import BaseRepository
from private_library.application import interfaces
from private_library.application.dataclasses import Book, Journal, User
from sqlalchemy import desc, or_, select


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

    def get_all(self) -> List[Book]:
        query = select(Book)
        return self.session.execute(query).scalars().all()

    def get_by_isbn13(self, isbn13: str) -> Optional[Book]:
        query = select(Book).where(Book.isbn13 == isbn13)
        return self.session.execute(query).scalars().one_or_none()

    def filter_by_price(self, price: str, query: object) -> object:
        if 'gte:' in price:
            price = float(price[4:])
            query = query.where(Book.price_USD >= price)
        elif 'lte:' in price:
            price = float(price[4:])
            query = query.where(Book.price_USD <= price)
        else:
            try:
                price = float(price)
                query = query.where(Book.price_USD <= price)
            except ValueError:
                pass
        return query

    def filter_by_authors(self, authors: str, query: object) -> List[Book]:
        query = query.where(Book.authors.ilike(f'%{authors}%'))
        return query

    def filter_by_publisher(self, publisher: str, query: object) -> object:
        query = query.where(Book.publisher.ilike(f'%{publisher}%'))
        return query

    def filter_by_keyword(self, keyword: str, query: object) -> object:
        query = query.where(
            or_(
                Book.desc.ilike(f'%{keyword}%'),
                Book.subtitle.ilike(f'%{keyword}%')
            )
        )
        return query

    def order_by(self, column: str, query: object) -> object:
        if column == 'price_USD':
            query = (query.order_by(Book.price_USD))
        if column == 'pages':
            query = (query.order_by(Book.pages))
        return query

    def get_top_three(self, tag: str) -> List[Book]:
        query = select(Book).where(Book.tag == tag)
        query = query.order_by(desc(Book.rating))
        query = query.order_by(Book.year).limit(3)
        return self.session.execute(query).scalars().all()

    def get_query(self) -> object:
        query = select(Book)
        return query

    def get_filter_data(self, query: object) -> List[Book]:
        return self.session.execute(query).scalars().all()


@component
class JournalRepo(BaseRepository, interfaces.JournalRepo):

    def get_by_id(self, id: int) -> Optional[Journal]:
        query = select(Journal).where(Journal.id == id)
        result = self.session.execute(query).scalars().one_or_none()
        return self._parse_date(result)

    def add(self, journal: Journal):
        self.session.add(journal)
        self.session.flush()

    def get_all(self) -> List[Journal]:
        query = select(Journal)
        results = self.session.execute(query).scalars().all()
        return list(map(self._parse_date, results))

    def get_by_user_id(self, user_id: int) -> List[Journal]:
        query = select(Journal).where(Journal.user_id == user_id)
        results = self.session.execute(query).scalars().all()
        return list(map(self._parse_date, results))

    def get_by_book_id(self, book_id: int) -> List[Journal]:
        query = select(Journal).where(Journal.book_id == book_id)
        results = self.session.execute(query).scalars().all()
        return list(map(self._parse_date, results))

    def get_active_record(self, user_id: int) -> Optional[Journal]:
        query = select(Journal).where(
            Journal.status == 'take', Journal.user_id == user_id
        )
        result = self.session.execute(query).scalars().one_or_none()
        return self._parse_date(result)

    @classmethod
    def _parse_date(cls, journal: Journal) -> Journal:
        if journal is not None:
            if isinstance(journal.taking_date, datetime):
                journal.taking_date = journal.taking_date.strftime(
                    '%Y-%m-%d %H:%M:%S'
                )

            if journal.timedelta is not None:
                journal.timedelta = str(journal.timedelta)

            if isinstance(journal.returning_date, datetime):
                journal.returning_date = journal.returning_date.strftime(
                    '%Y-%m-%d %H:%M:%S'
                )
        return journal
