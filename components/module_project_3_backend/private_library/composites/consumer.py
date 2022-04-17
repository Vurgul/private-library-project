from evraz.classic.sql_storage import TransactionContext
from kombu import Connection
from private_library.adapters import database, message_bus, private_library_api
from private_library.application import services
from sqlalchemy import create_engine


class Settings:
    db = database.Settings()
    message_bus = message_bus.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL, echo=True)    # , echo=True
    database.metadata.create_all(engine)

    context = TransactionContext(bind=engine)

    books_repo = database.repositories.BooksRepo(context=context)
    users_repo = database.repositories.UsersRepo(context=context)


class Application:
    books = services.BookServices(
        book_repo=DB.books_repo,
        user_repo=DB.users_repo,
    )


class MessageBus:
    connection = Connection(Settings.message_bus.BROKER_URL)

    consumer = message_bus.create_consumer(connection, Application.books)

    @staticmethod
    def declare_scheme():
        message_bus.broker_scheme.declare(MessageBus.connection)


class Aspects:
    services.join_points.join(DB.context)
    private_library_api.join_points.join(DB.context)


if __name__ == '__main__':
    MessageBus.declare_scheme()
    MessageBus.consumer.run()
