import pytest
import transaction
import datetime
import os

from pyramid import testing

from ..models import (
    Entry,
    get_engine,
    get_session_factory,
    get_tm_session,
)
from ..models.meta import Base

DB_SETTINGS = {'sqlalchemy.url': 'postgres://james@localhost:5432/test_lj_step3'}


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


def test_model_gets_added(new_session):
    '''Checks a modle gets put into the DB'''
    assert len(new_session.query(Entry).all()) == 0
    model = Entry(title="Bob", date=datetime.datetime.now(), body='Here is a body')
    new_session.add(model)
    new_session.flush()
    assert len(new_session.query(Entry).all()) == 1


def dummy_request(new_session):
    return testing.DummyRequest(dbsession=new_session)


def test_my_view(new_session):
    '''Checks a title we enter to the DB gets output on the homepage'''
    from ..views.default import home_view
    new_session.add(Entry(title="James", date=datetime.datetime.now(), body='Lady lah'))
    new_session.flush()
    http_request = dummy_request(new_session)
    result = home_view(http_request)
    assert result['entries'][0].title == "James"


def test_detail_view(new_session):
    '''Checks respons to reques with id 1 contains a the body I added'''
    from ..views.default import detail_view
    new_session.add(Entry(title="James", date=datetime.datetime.now(), body='Lady lahfff'))
    request = testing.DummyRequest(dbsession=new_session)
    request.matchdict['id'] = 1
    result = detail_view(request)
    assert result['single_entry'].body == 'Lady lahfff'


def test_new_list_view():
    '''Test create view.'''
    from ..views.default import new_list_view
    request = testing.DummyRequest()
    new_list_view(request)
    assert request.response.status_code == 200


def test_edit_view(new_session):
    '''Checks respons to reques with id 1 contains a the title I added'''
    from ..views.default import edit_view
    request = testing.DummyRequest(dbsession=new_session)
    new_session.add(Entry(title="James", date=datetime.datetime.now(), body='Lady lah'))
    request.matchdict['id'] = 1
    result = edit_view(request)
    assert result['edit_entry'].title == 'James'


# -------Functional Tests----------


@pytest.fixture()
def testapp(sqlengine, setup_test_env):
    '''Setup TestApp.'''
    from lj_step3 import main
    app = main({}, **DB_SETTINGS)
    from webtest import TestApp
    return TestApp(app)


def test_layout_root_home(testapp, populated_db):
    '''Test layout root of home route.'''
    response = testapp.get('/', status=200)
    assert b'Vic Week 2 Day 5' in response.body


def test_layout_root_create(testapp):
    '''Test layout root of create route.'''
    response = testapp.get('/new', status=200)
    assert response.html.find("textarea")


def test_layout_root_edit(testapp, populated_db):
    '''Test layout root of edit route.'''
    response = testapp.get('/edit/1', status=200)
    html = response.html
    assert html.find("h1")


def test_layout_root_detail(testapp, populated_db):
    '''Test layout root of detail route.'''
    response = testapp.get('/detail/1', status=200)
    html = response.html
    assert html.find("p")


def test_root_contents_home(testapp, populated_db):
    '''Test contents of root page contain as many <article> as journal entries.'''
    response = testapp.get('/', status=200)
    html = response.html
    assert len(html.findAll("h2")) == 1


def test_root_contents_detail(testapp, populated_db):
    '''Test contents of detail page contains <p> in detail content.'''
    response = testapp.get('/detail/1', status=200)
    assert b"James is being awesome." in response.body

