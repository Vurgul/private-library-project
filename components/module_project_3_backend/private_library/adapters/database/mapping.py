from private_library.application import dataclasses
from sqlalchemy.orm import registry, relationship

from . import tables

mapper = registry()

mapper.map_imperatively(dataclasses.User, tables.users)
mapper.map_imperatively(dataclasses.Book, tables.books)
mapper.map_imperatively(
    dataclasses.Journal,
    tables.journal,
    properties={
        'user': relationship(
            dataclasses.User, uselist=False, lazy='joined'
        ),
        'book': relationship(
            dataclasses.Book, uselist=False, lazy='joined'
        ),
    }
)
