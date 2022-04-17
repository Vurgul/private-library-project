import jwt
from attr import asdict
from evraz.classic.components import component
from evraz.classic.http_auth import authenticate, authenticator_needed
from private_library.application import services

from .join_points import join_point


@component
class Authorization:
    authorization: services.Authorization

    @join_point
    def on_post_registration(self, request, response):
        self.authorization.add_user(**request.media)

    @join_point
    def on_post_authentication(self, request, response):
        """ Прохождение аутентификации -> авторизация"""
        user = self.authorization.authentication(**request.params)
        token = jwt.encode(
            {
                'sub': user.id,
                'login': user.login,
                'name': user.login,
                'group': 'User'
            },
            'auth_secret_key',
            algorithm='HS256'
        )
        response.media = {'token': token}


@authenticator_needed
@component
class Library:
    library: services.Library

    @join_point
    def on_get_books(self, request, response):
        """Получить информацию о всех книгах"""
        books = self.library.take_books_info()
        response.media = [asdict(book) for book in books]

    @join_point
    @authenticate
    def on_get_users(self, request, response):
        """Получить информацию о пользователях"""
        users = self.library.take_users_info()
        response.media = [
            {
                'login': user.login,
                'id': user.id
            } for user in users
        ]

    @join_point
    @authenticate
    def on_get_books_filter(self, request, response):
        """Получить информацию о всех книгах с использованием фильтрации"""
        books = self.library.take_books_with_filter_and_sort(**request.params)
        response.media = [asdict(book) for book in books]

    @join_point
    @authenticate
    def on_get_book(self, request, response):
        """Получить информацию о книге"""
        book = self.library.take_book_info(**request.params)
        response.media = asdict(book)

    @join_point
    @authenticate
    def on_get_journal(self, request, response):
        """Получить список ранее взятых книг"""
        journal_records = self.library.take_self_journal(
            user_id=request.context.client.user_id
        )
        response.media = [asdict(record) for record in journal_records]

    @join_point
    @authenticate
    def on_get_active_book(self, request, response):
        """Получить активную книгу"""
        book = self.library.take_active_book(
            user_id=request.context.client.user_id
        )
        response.media = asdict(book)

    @join_point
    @authenticate
    def on_post_reserve_book(self, request, response):
        """Забронировать книгу"""
        self.library.open_reserve_book(
            user_id=request.context.client.user_id,
            **request.media,
        )

    @join_point
    @authenticate
    def on_post_return_book(self, request, response):
        """Вернуть книгу"""
        debt = self.library.close_reserve_book(
            user_id=request.context.client.user_id
        )
        if debt is not None:
            response.media = {'Booking overdue': debt}

    @join_point
    @authenticate
    def on_post_buy_book(self, request, response):
        """Выкупить книгу"""
        self.library.buy_book(user_id=request.context.client.user_id)

    @join_point
    def on_get_journal_records(self, request, response):
        """Просмотр всех записей о взятии и покупки книг """
        records = self.library.get_all_journal_records()
        response.media = [asdict(record) for record in records]
