from datetime import datetime

from sqlalchemy import (Column, Integer, MetaData,
                        String, Table, Float, ForeignKey, DateTime
                        )

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

metadata = MetaData(naming_convention=naming_convention)

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(128), nullable=False),
    Column('age', Integer, nullable=True),
    Column('login', String(128), nullable=False, unique=True),
    Column('password', String(128), nullable=False),
)

books = Table(
    'books',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(1000), nullable=False),
    Column('authors', String(1000), nullable=False),
    Column('publisher', String(1000), nullable=False),
    Column('language', String(1000), nullable=False),
    Column('isbn13', String(1000), nullable=False),
    Column('pages', Integer, nullable=False),
    Column('year', Integer, nullable=True),
    Column('rating', Float, nullable=False),
    Column('desc', String(1000), nullable=True),
    Column('price_USD', Float, nullable=False),
)

journal = Table(
    'journal',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id'), nullable=False),
    Column('book_id', ForeignKey('books.id'), nullable=False),
    Column('action', String(128), nullable=False),
    Column('taking_date', DateTime, nullable=False, default=datetime.utcnow()),
    Column(
        'returning_date',
        DateTime,
        nullable=True,
        default=datetime.utcnow()
    ),
)
