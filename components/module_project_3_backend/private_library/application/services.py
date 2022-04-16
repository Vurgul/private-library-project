from datetime import datetime, timedelta
from typing import List, Optional

import requests
from evraz.classic.app import DTO, validate_with_dto
from evraz.classic.aspects import PointCut
from evraz.classic.components import component
from pydantic import validate_arguments

from . import errors, interfaces
from .dataclasses import Book, Journal, User

join_points = PointCut()
join_point = join_points.join_point


class UserInfo(DTO):
    login: str
    password: str
    name: str
    age: Optional[int]
    id: Optional[int]


class UserUpDateInfo(DTO):
    login: Optional[str]
    password: Optional[str]
    name: Optional[str]
    age: Optional[int]
    id: int


class JournalReload(DTO):
    returning_date: Optional[datetime]
    status: str


class JournalInfo(DTO):
    user_id: int
    book_id: int
    status: str
    id: Optional[int]
    taking_date: Optional[datetime]
    timedelta: Optional[timedelta]
    returning_date: Optional[datetime]


class BookInfo(DTO):
    id: Optional[int]
    title: str
    subtitle: str
    authors: str
    publisher: str
    language: str
    isbn13: str
    pages: int
    year: int
    rating: float
    price_USD: float
    desc: Optional[str]
    tag: str


class FilterBook(DTO):
    price_USD: Optional[str]
    keyword: Optional[str]
    authors: Optional[str]
    publisher: Optional[str]
    order_by: Optional[str]


@component
class Authorization:
    user_repo: interfaces.UsersRepo

    @join_point
    @validate_with_dto
    def add_user(self, user_info: UserInfo):
        if self.user_repo.get_by_login(user_info.login) is not None:
            raise errors.NotUniqueLogin(login=user_info.login)
        user = user_info.create_obj(User)
        self.user_repo.add(user)

    @join_point
    @validate_arguments
    def get_user_info(self, user_id: int) -> User:
        user = self.user_repo.get_by_id(user_id)
        if user is None:
            raise errors.NoUser(id=user_id)
        return user

    @join_point
    @validate_arguments
    def authentication(self, login: str, password: str) -> User:
        user = self.user_repo.get_by_user_data(login, password)
        if user is None:
            raise errors.IncorrectData()
        return user


@component
class BookServices:
    book_repo: interfaces.BooksRepo
    user_repo: interfaces.UsersRepo

    def take_message(self, tag: str):
        url_search = 'https://api.itbook.store/1.0/search'
        url_books_isbn = 'https://api.itbook.store/1.0/books'
        res = requests.get(f'{url_search}/{tag}').json()
        count_search_result = int(res['total'])

        if count_search_result >= 41:
            page_number = 5
        else:
            page_number = count_search_result // 10 + 1

        for i in range(1, page_number+1):
            res_page = requests.get(f'{url_search}/{tag}/{i}').json()
            books = res_page['books']
            for book in books:
                isbn13 = book['isbn13']
                book_info = requests.get(f'{url_books_isbn}/{isbn13}').json()
                book_info['price_USD'] = float(book_info['price'][1:])
                book_info['tag'] = tag
                self.add_book(**book_info)
        self.send_message(tag)

    @join_point
    @validate_with_dto
    def add_book(self, book_info: BookInfo):
        if self.book_repo.get_by_isbn13(book_info.isbn13) is None:
            book = book_info.create_obj(Book)
            self.book_repo.add(book)

    @join_point
    def send_message(self, tag: str):
        users = self.user_repo.get_all()
        for user in users:
            books = self.book_repo.get_top_three(tag)
            print('-----------')
            print(f'{user.login}, книги  по теме {tag} для тебя: {books}')
            print('-----------')


@component
class Library:
    user_repo: interfaces.UsersRepo
    book_repo: interfaces.BooksRepo
    journal_repo: interfaces.JournalRepo

    @join_point
    @validate_arguments
    def take_users_info(self) -> List[User]:
        users = self.user_repo.get_all()
        return users

    @join_point
    @validate_arguments
    def take_books_info(self) -> List[Book]:
        books = self.book_repo.get_all()
        return books

    @join_point
    @validate_with_dto
    def take_books_with_filter_and_sort(
        self, filter_date: FilterBook
    ) -> List[Book]:

        books = self.book_repo.get_query()
        if filter_date.price_USD is not None:
            books = self.book_repo.filter_by_price(
                filter_date.price_USD,
                books,
            )
        if filter_date.publisher is not None:
            books = self.book_repo.filter_by_publisher(
                filter_date.publisher,
                books
            )
        if filter_date.authors is not None:
            books = self.book_repo.filter_by_authors(filter_date.authors, books)
        if filter_date.keyword is not None:
            books = self.book_repo.filter_by_keyword(filter_date.keyword, books)

        if filter_date.order_by is not None:
            books = self.book_repo.order_by(filter_date.order_by, books)

        books = self.book_repo.get_filter_data(books)

        return books

    @join_point
    @validate_arguments
    def take_book_info(self, book_id: int) -> Book:
        book = self.book_repo.get_by_id(book_id)
        if book is None:
            raise errors.NoBook(id=book_id)
        return book

    @join_point
    @validate_arguments
    def take_self_journal(self, user_id: int) -> List[Journal]:
        journal_records = self.journal_repo.get_by_user_id(user_id)
        return journal_records

    @join_point
    @validate_arguments
    def take_active_book(self, user_id: int) -> Book:
        journal_record = self.journal_repo.get_active_record(user_id)
        if journal_record is None:
            raise errors.NoJournal(id=user_id)
        book = self.take_book_info(journal_record.book_id)
        return book

    @join_point
    @validate_arguments
    def open_reserve_book(self, user_id: int, book_id: int, time_delta=7):
        book = self.take_book_info(book_id)

        journal_records = self.take_self_journal(user_id)
        for journal_record in journal_records:
            if journal_record.status == 'take':
                raise errors.HaveActiveBook(id=journal_record.book_id)

        journal_records = self.journal_repo.get_by_book_id(book.id)
        for journal_record in journal_records:
            if journal_record.status == 'take':
                raise errors.BookBusy(id=book_id)
            if journal_record.status == 'buy':
                raise errors.BookBuy(id=book_id)

        journal_info = JournalInfo(
            user_id=user_id,
            book_id=book_id,
            status='take',
            timedelta=timedelta(days=time_delta),
        )
        self.create_journal_record(**journal_info.dict())

    @join_point
    @validate_with_dto
    def create_journal_record(self, journal_info: JournalInfo):
        journal_record = journal_info.create_obj(Journal)
        self.journal_repo.add(journal_record)

    @join_point
    @validate_arguments
    def close_reserve_book(self, user_id: int):
        journal_record = self._validate_journal_record_take_book_exists(user_id)

        modern_journal_record = JournalReload(
            returning_date=datetime.utcnow(),
            status='return'
        )
        modern_journal_record.populate_obj(journal_record)

    @join_point
    @validate_arguments
    def buy_book(self, user_id: int):
        journal_record = self._validate_journal_record_take_book_exists(user_id)

        modern_journal_record = JournalReload(status='buy')
        modern_journal_record.populate_obj(journal_record)

    def _validate_journal_record_take_book_exists(
        self, user_id: int
    ) -> Optional[Journal]:

        journal_record = self.journal_repo.get_active_record(user_id)
        if journal_record is None:
            raise errors.NoJournal(id=user_id)
        return journal_record

    @join_point
    def get_all_j(self):
        j = self.journal_repo.get_all()
        return j
