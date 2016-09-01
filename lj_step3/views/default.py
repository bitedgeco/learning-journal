from pyramid.view import view_config
from ..models import Entry
from pyramid.response import Response
from sqlalchemy import desc
import datetime
from pyramid.httpexceptions import HTTPFound


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


@view_config(route_name='edit', renderer='templates/edit.jinja2')
def edit_view(request):
    query = request.dbsession.query(Entry)
    edit_entry = query.filter_by(id=request.matchdict['id']).first()
    if request.method == 'POST':
        edit_entry.title = request.POST["title"]
        edit_entry.body = request.POST["body"]
        edit_entry = Entry(title=edit_entry.title, body=edit_entry.body, date=edit_entry.date)
        return HTTPFound(location=request.route_url('home'))

    return {'edit_entry': edit_entry}


@view_config(route_name='new', renderer='templates/new.jinja2')
def new_list_view(request):
    if request.method == 'POST':
        new = Entry(title=request.POST['title'], date=datetime.datetime.now(), body=request.POST['body'])
        request.dbsession.add(new)
        return HTTPFound(location=request.route_url('home'))
    return {}



