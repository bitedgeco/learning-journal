from ..models.meta import Base
from passlib.apps import custom_app_context as pwd_context
import transaction
import os
from ..models import (
    Entry,
    get_engine,
    get_session_factory,
    get_tm_session,
)
import pytest
import datetime
from pyramid import testing


DB_SETTINGS = {'sqlalchemy.url': 'postgres://james@localhost:5432/test_lj_step3'}


@pytest.fixture(scope='session')
def auth_env():
    username = 'billy'
    password = 'secret password'
    os.environ['AUTH_USERNAME'] = username
    os.environ['AUTH_PASSWORD'] = pwd_context.encrypt(password)
    return username, password


@pytest.fixture(scope='function')
def auth_app(testapp, auth_env):
    username, password = auth_env
    auth_data = {
        'username': username,
        'password': password
    }
    testapp.post('/login', auth_data, status='3*')
    return testapp


@pytest.fixture(scope="session")
def setup_test_env():
    os.environ["DATABASE_URL"] = 'postgres://james@localhost:5432/test_lj_step3'


@pytest.fixture(scope="function")
def sqlengine(request):
    config = testing.setUp(settings=DB_SETTINGS)
    config.include("..models")
    settings = config.get_settings()
    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    def teardown():
        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture(scope="function")
def new_session(sqlengine, request):
    session_factory = get_session_factory(sqlengine)
    session = get_tm_session(session_factory, transaction.manager)

    def teardown():
        transaction.abort()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope="function")
def populated_db(request, sqlengine):
    session_factory = get_session_factory(sqlengine)
    session = get_tm_session(session_factory, transaction.manager)

    with transaction.manager:
        session.add(Entry(title="Vic Week 2 Day 5", body="This is a test entry, James is being awesome.", date=datetime.datetime.utcnow()))

    def teardown():
        with transaction.manager:
            session.query(Entry).delete()

    request.addfinalizer(teardown)
