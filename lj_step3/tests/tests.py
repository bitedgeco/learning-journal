import os
from ..models import Entry
import pytest
import datetime
from pyramid import testing

DB_SETTINGS = {'sqlalchemy.url': 'postgres://james@localhost:5432/test_lj_step3'}


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


def test_new_view():
    '''Test create view.'''
    from ..views.default import new_view
    request = testing.DummyRequest()
    new_view(request)
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
    response = testapp.get('/new', status=403)
    assert response.status_code == 403


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

# -----Chris' security tests--------


def test_private_view_accessible(auth_app):
    '''tests if authenticated app can access restricted page.'''
    response = auth_app.get('/edit/1', status=200)
    assert response.status_code == 200


def test_layout_root__auth_edit(auth_app, populated_db):
    '''Test layout of edit route.'''
    response = auth_app.get('/edit/1', status=200)
    assert response.html.find("h1")


def test_layout_root_create_auth(auth_app):
    '''Test layout root of create route.'''
    response = auth_app.get('/new', status=200)
    assert response.html.find("textarea")


def test_auth_user_name_exists(auth_env):
    '''test username exists'''
    assert os.environ.get('AUTH_USERNAME') is not None


def test_auth_username_is_not_empty(auth_env):
    '''test username is not an empty string'''
    assert os.environ.get('AUTH_USERNAME') != ''


def test_auth_user_pwd_exists(auth_env):
    '''test password exists'''
    assert os.environ.get('AUTH_PASSWORD') is not None


def test_auth_pwd_is_not_empty(auth_env):
    '''test password is not an empty string'''
    assert os.environ.get('AUTH_PASSWORD') != ''


def test_cred_is_good(auth_env):
    '''test check_credentials passes when given good credentials'''
    from ..security import check_credentials
    actual_username, actual_password = auth_env
    assert check_credentials(actual_username, actual_password)


def test_pwd_is_bad_fails(auth_env):
    '''test check_credentials fails when given bad password'''
    from ..security import check_credentials
    actual_username, actual_password = auth_env
    fake_password = actual_password + 'nope'
    assert not check_credentials(actual_username, fake_password)


def test_user_is_bad_fails(auth_env):
    '''test check_credentials fails when given bad password'''
    from ..security import check_credentials
    actual_username, actual_password = auth_env
    fake_username = actual_username + 'nope'
    assert not check_credentials(fake_username, actual_password)


def test_login_view_succeeds(testapp):
    '''test check_credentials fails when given bad password'''
    response = testapp.get('/login')
    assert response.status_code == 200


def test_login_view_post_success(auth_app, auth_env):
    '''Tests that successfull login redirects'''
    username, password = auth_env
    auth_data = {
        'username': username,
        'password': password
    }
    response = auth_app.post('/login', auth_data, status='3*')
    assert response.status_code == 302


def test_priv_view_success_auth(auth_app):
    '''tests loged in act can access restricted new page'''
    response = auth_app.get('/new')
    assert response.status_code == 200


def test_post_log_has_cookie(auth_app, auth_env):
    '''tests an appropreate cookie exists after login'''
    username, password = auth_env
    auth_data = {
        'username': username,
        'password': password
    }
    response = auth_app.post('/login', auth_data, status='3*')
    # import pdb; pdb.set_trace()
    for header_name, header_value in response.headerlist:
        if header_name == 'Set-Cookie' and header_value.startswith('auth_tkt'):
            break
    else:
        assert False


def test_check_fails_if_stored_password_is_plain_txt(auth_env):
    '''tests password is encrypted'''
    from ..security import check_credentials
    actual_username, actual_password = auth_env
    os.environ['AUTH_PASSWORD'] = actual_password
    assert not check_credentials(actual_username, actual_password)
