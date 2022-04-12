from typing import List, Optional

from evraz.classic.app import DTO, validate_with_dto
from evraz.classic.aspects import PointCut
from evraz.classic.components import component
from evraz.classic.messaging import Message, Publisher
from pydantic import validate_arguments

from . import errors, interfaces
from .dataclasses import User

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
class Library:
    user_repo: interfaces.UsersRepo
    book_repo: interfaces.BooksRepo
    journal_repo: interfaces.JournalRepo

    @join_point
    @validate_with_dto
    def take_books_info(self):
        pass

    @join_point
    @validate_with_dto
    def take_book_info(self):
        pass

    @join_point
    @validate_with_dto
    def take_self_journal(self):
        pass

    @join_point
    @validate_with_dto
    def take_active_book(self):
        pass

    @join_point
    @validate_with_dto
    def open_reserve_book(self):
        pass

    @join_point
    @validate_with_dto
    def close_reserve_book(self):
        pass

    @join_point
    @validate_with_dto
    def buy_book(self):
        pass
