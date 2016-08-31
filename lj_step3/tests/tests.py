import pytest
import transaction
import datetime

from pyramid import testing

from ..models import (
    Entry,
    get_engine,
    get_session_factory,
    get_tm_session,
)
from ..models.meta import Base


@pytest.fixture(scope="session")
def sqlengine(request):
    config = testing.setUp(settings={
        'sqlalchemy.url': 'sqlite:///:memory:'
    })
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


def test_model_gets_added(new_session):
    assert len(new_session.query(Entry).all()) == 0
    model = Entry(title="Bob", date=datetime.datetime.now(), body='Here is a body')
    new_session.add(model)
    new_session.flush()
    assert len(new_session.query(Entry).all()) == 1


def dummy_request(new_session):
    return testing.DummyRequest(dbsession=new_session)


def test_my_view(new_session):
    from ..views.default import home_view
    new_session.add(Entry(title="James", date=datetime.datetime.now(), body='Lady lah'))
    new_session.flush()
    http_request = dummy_request(new_session)
    result = home_view(http_request)
    assert result['entries'][0].title == "James"


def test_detail_view(new_session):
    '''Checks respons to reques with id 13 contains a title'''
    from ..views.default import detail_view
    request = testing.DummyRequest(dbsession=new_session)
    new_session.add(Entry(title="James", date=datetime.datetime.now(), body='Lady lah'))
    request.matchdict['id'] = 1
    result = detail_view(request)
    assert result['single_entry'].body == 'Lady lah'


# *****Tests not yet working ******

# @pytest.fixture()
# def testapp():
#     '''makes test app for testing'''
#     from lj_step3 import main
#     app = main({})
#     from webtest import TestApp
#     return TestApp(app)


# def test_layout_root(testapp):
#     '''Test body contains paragraph tags'''
#     response = testapp.get('/', status=200)
#     assert b'<p>' in response.body


# def test_root_contents(testapp):
#     '''Test that the contents of the root page contains as many <h2> tags as journal entries.'''
#     from .views import ENTRIES
#     response = testapp.get('/', status=200)
#     html = response.html
#     assert len(ENTRIES) == len(html.findAll("h2"))

