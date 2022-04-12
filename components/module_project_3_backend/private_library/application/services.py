from typing import List, Optional

from evraz.classic.app import DTO, validate_with_dto
from evraz.classic.aspects import PointCut
from evraz.classic.components import component
from evraz.classic.messaging import Message, Publisher
from pydantic import validate_arguments

from . import errors, interfaces
from .dataclasses import User, Book, Journal

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
    user_id: int
    book_id: int
    id: Optional[int]


@component
class Authorization:
    user_repo: interfaces.UsersRepo

    @join_point
    @validate_with_dto
    def add_user(self, user_info: UserInfo):
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
        return user


@component
class UserService:
    user_repo: interfaces.UsersRepo
    publisher: Publisher

    @join_point
    @validate_arguments
    def get_user_info(self, user_id: int) -> User:
        user = self.user_repo.get_by_id(user_id)
        if user is None:
            raise errors.NoUser(id=user_id)

        return user

    @join_point
    def get_users_info(self) -> List[User]:
        users = self.user_repo.get_all()
        return users

    @join_point
    @validate_with_dto
    def create_user(self, user_info: UserInfo) -> User:
        print('TEST CONNECTION')
        user = user_info.create_obj(User)
        self.user_repo.add(user)

        if self.publisher:
            self.publisher.plan(
                Message(
                    'our_exchange',
                    {
                        'action': 'create',
                        'object_type': 'user',
                        'object_id': user.id,
                    }
                )
            )

        return user

    @join_point
    @validate_arguments
    def update_user_info(self, user_id: int, **kwargs) -> User:
        user = self.get_user_info(user_id)
        modern_user = UserUpDateInfo(id=user_id, **kwargs)
        modern_user.populate_obj(user)

        return user

    @join_point
    @validate_arguments
    def delete_user(self, user_id: int):
        user = self.get_user_info(user_id)

        if self.publisher:
            self.publisher.plan(
                Message(
                    'our_exchange',
                    {
                        'action': 'delete',
                        'object_type': 'user',
                        'object_id': user.id,
                    }
                )
            )

        self.user_repo.remove(user)


@component
class BookServices:
    book_repo: interfaces.BooksRepo

    @join_point
    def take_message(self): ...


@component
class Library:
    user_repo: interfaces.UsersRepo
    book_repo: interfaces.BooksRepo
    journal_repo: interfaces.JournalRepo

    @join_point
    @validate_arguments
    def take_books_info(self) -> List[Book]:
        books = self.book_repo.get_all()
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
        if journal_record in None:
            raise errors.NoJournal(id=user_id)
        book = self.take_book_info(journal_record.book_id)
        return book

    @join_point
    @validate_arguments
    def open_reserve_book(self, user_id: int, book_id: int):
        journal_records = self.journal_repo.get_by_book_id(book_id)

        for journal_record in journal_records:
            if journal_record.action != 'return':
                raise errors.BookBusy(id=book_id)


    @join_point
    @validate_arguments
    def close_reserve_book(self):
        pass

    @join_point
    @validate_arguments
    def buy_book(self):
        pass


