import jwt
from attr import asdict
from evraz.classic.components import component
from private_library.application import services
from evraz.classic.http_auth import authenticate, authenticator_needed
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
        user = self.authorization.authentication(
            **request.params
        )
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
class Users:
    users: services.UserService

    @join_point
    def on_get_user_info(self, request, response):
        """Получить информацию о пользователе"""
        user = self.users.get_user_info(
            **request.params
        )
        response.media = asdict(user)

    @join_point
    def on_get_users(self, request, response):
        """Получить информацию о всех пользователях"""
        users = self.users.get_users_info()
        response.media = [asdict(user) for user in users]


    @join_point
    def on_post_add_user(self, request, response):
        """Добавить пользователя"""
        user = self.users.create_user(
            **request.media
        )

        response.media = {
            'user_id': user.id
        }

    @join_point
    def on_post_edit_user(self, request, response):
        """Изменение данных пользователя"""
        user = self.users.update_user_info(
            **request.media
        )
        response.media = asdict(user)

    @join_point
    def on_post_delete_user(self, request, response):
        """ Удалить пользователя"""
        self.users.delete_user(
            **request.media
        )


@authenticator_needed
@component
class Library:
    library: services.Library

    @join_point
    def on_get_books(self, request, response):
        """Получить информацию о всех книгах"""
        books = self.library.take_books_info()
        print(books)
        response.media = [asdict(book) for book in books]

    @join_point
    @authenticate
    def on_get_book(self, request, response):
        """Получить информацию о книге"""
        book = self.library.take_book_info(
            **request.media
        )
        response.media = asdict(book)

    @join_point
    @authenticate
    def on_get_journal(self, request, response):
        """Получить список ранее взятых книг"""

    @join_point
    @authenticate
    def on_get_active_book(self, request, response):
        """Получить активную книгу"""

    @join_point
    @authenticate
    def on_post_reserve_book(self, request, response):
        """Забронировать книгу"""

    @join_point
    @authenticate
    def on_post_return_book(self, request, response):
        """Вернуть книгу"""

    @join_point
    @authenticate
    def on_post_buy_book(self, request, response):
        """Выкупить книгу"""
