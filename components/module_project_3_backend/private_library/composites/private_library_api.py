from evraz.classic.messaging_kombu import KombuPublisher
from evraz.classic.sql_storage import TransactionContext
from kombu import Connection
from sqlalchemy import create_engine
from private_library.adapters import database, message_bus, private_library_api
from private_library.application import services


class Settings:
    db = database.Settings()
    private_library_api = private_library_api.Settings()
    message_bus = message_bus.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL, echo=True)  # , echo=True
    database.metadata.create_all(engine)

    context = TransactionContext(bind=engine)

    users_repo = database.repositories.UsersRepo(context=context)
    books_repo = database.repositories.BooksRepo(context=context)
    journal_repo = database.repositories.JournalRepo(context=context)


class MessageBus:
    connection = Connection(Settings.message_bus.BROKER_URL)
    message_bus.broker_scheme.declare(connection)

    publisher = KombuPublisher(
        connection=connection,
        scheme=message_bus.broker_scheme,
        messages_params={
            'our_exchange': {
                'exchange': 'our_exchange',
                'routing_key': 'project_queue',
            }
        }
    )


class Application:
    authorization = services.Authorization(
        user_repo=DB.users_repo,
    )

    users = services.UserService(
        user_repo=DB.users_repo,
        publisher=MessageBus.publisher,
    )
    library = services.Library(
        user_repo=DB.users_repo,
        book_repo=DB.books_repo,
        journal_repo=DB.journal_repo,
    )
    books = services.BookServices(
        book_repo=DB.books_repo,
    )


class Aspects:
    services.join_points.join(DB.context)
    private_library_api.join_points.join(MessageBus.publisher, DB.context)


app = private_library_api.create_app(
    authorization=Application.authorization,
    users=Application.users,
    library=Application.library,
)

