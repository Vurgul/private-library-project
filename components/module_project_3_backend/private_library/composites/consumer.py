from evraz.classic.sql_storage import TransactionContext
from kombu import Connection
from sqlalchemy import create_engine
from private_library.adapters import database, message_bus
from private_library.application import services


class Settings:
    db = database.Settings()
    message_bus = message_bus.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL, echo=True)  # , echo=True
    database.metadata.create_all(engine)

    context = TransactionContext(bind=engine)

    books_repo = database.repositories.BooksRepo(context=context)


class Application:
    books = services.BookServices(
        issue_repo=DB.books_repo,
    )


class MessageBus:
    connection = Connection(Settings.message_bus.BROKER_URL)

    consumer = message_bus.create_consumer(connection, Application.books)

    @staticmethod
    def declare_scheme():
        message_bus.broker_scheme.declare(MessageBus.connection)


if __name__ == '__main__':
    MessageBus.declare_scheme()
    MessageBus.consumer.run()
