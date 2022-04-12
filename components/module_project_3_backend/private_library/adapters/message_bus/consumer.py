from evraz.classic.messaging_kombu import KombuConsumer
from private_library.application import services
from kombu import Connection

from .scheme import broker_scheme


def create_consumer(
    connection: Connection, books: services.BookServices
) -> KombuConsumer:

    consumer = KombuConsumer(connection=connection, scheme=broker_scheme)

    consumer.register_function(
        books.take_message,
        'ProjectQueue',
    )

    return consumer
