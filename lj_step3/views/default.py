from pyramid.view import view_config
from ..models import Entry
from pyramid.response import Response
from sqlalchemy import desc
import datetime
from pyramid.httpexceptions import HTTPFound
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
# from test_transactions.security import check_credentials


@view_config(route_name='login', renderer='templates/login.jinja2')
def login(request):
    if request.method == 'POST':
        username = request.params.get('username', '')
        password = request.params.get('password', '')
        if check_credentials(username, password):
            headers = remember(request, username)
            return HTTPFound(location=request.route_url('home'), headers=headers)
    return {}


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)


@view_config(route_name='home', renderer='templates/home.jinja2')
def home_view(request):
    query = request.dbsession.query(Entry)
    all_entries = query.order_by(desc(Entry.date)).all()
    return {'entries': all_entries}


@view_config(route_name='detail', renderer='templates/detail.jinja2')
def detail_view(request):
    query = request.dbsession.query(Entry)
    single_entry = query.filter_by(id=request.matchdict['id']).first()
    return {'single_entry': single_entry}


@view_config(route_name='edit', renderer='templates/edit.jinja2', permission='secret')
def edit_view(request):
    query = request.dbsession.query(Entry)
    edit_entry = query.filter_by(id=request.matchdict['id']).first()
    if request.method == 'POST':
        edit_entry.title = request.POST["title"]
        edit_entry.body = request.POST["body"]
        edit_entry = Entry(title=edit_entry.title, body=edit_entry.body, date=edit_entry.date)
        return HTTPFound(location=request.route_url('home'))

    return {'edit_entry': edit_entry}


@view_config(route_name='new', renderer='templates/new.jinja2', permission='secret')
def new_view(request):
    if request.method == 'POST':
        new = Entry(title=request.POST['title'], date=datetime.datetime.now(), body=request.POST['body'])
        request.dbsession.add(new)
        return HTTPFound(location=request.route_url('home'))
    return {}



