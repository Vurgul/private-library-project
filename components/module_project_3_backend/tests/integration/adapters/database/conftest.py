import os

import pytest
from evraz.classic.sql_storage import TransactionContext
from private_library.adapters.database.tables import metadata
from sqlalchemy import create_engine


@pytest.fixture(scope='session')
def engine():
    user = os.getenv('PS_USER', 'postgres')
    password = os.getenv('PS_PASSWORD', '1988723')
    host = os.getenv('PS_HOST', 'localhost')
    port = os.getenv('PS_PORT', '5432')
    database = os.getenv('PS_DATABASE', 'test_private_library')

    engine = create_engine(
        f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
    )

    for key, value in metadata.tables.items():
        value.schema = None

    metadata.create_all(engine)

    return engine


@pytest.fixture(scope='session')
def transaction_context(engine):
    return TransactionContext(bind=engine)


@pytest.fixture(scope='function')
def session(transaction_context: TransactionContext):
    session = transaction_context.current_session

    if session.in_transaction():
        session.begin_nested()
    else:
        session.begin()

    yield session

    session.rollback()
