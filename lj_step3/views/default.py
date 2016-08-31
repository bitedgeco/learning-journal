from pyramid.view import view_config
from ..models import Entry
from sqlalchemy.exc import DBAPIError
from pyramid.response import Response
from sqlalchemy import desc
import datetime
from pyramid.httpexceptions import HTTPFound


@view_config(route_name='home', renderer='templates/home.jinja2')
def home_view(request):
    try:
        query = request.dbsession.query(Entry)
        all_entries = query.order_by(desc(Entry.date)).all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'entries': all_entries}


@view_config(route_name='detail', renderer='templates/detail.jinja2')
def detail_view(request):
    try:
        query = request.dbsession.query(Entry)
        single_entry = query.filter_by(id=request.matchdict['id']).first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'single_entry': single_entry}


@view_config(route_name='edit', renderer='templates/edit.jinja2')
def edit_view(request):
    try:
        query = request.dbsession.query(Entry)
        edit_entry = query.filter_by(id=request.matchdict['id']).first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'edit_entry': edit_entry}


@view_config(route_name='new', renderer='templates/new.jinja2')
def new_list_view(request):
    if request.method == 'POST':
        new = Entry(title=request.POST['title'], date=datetime.datetime.now(), body=request.POST['body'])
        request.dbsession.add(new)
        return HTTPFound(location='/')
    return {}

db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_lj-step3_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

# from pyramid.response import Response
# from pyramid.view import view_config

# from sqlalchemy.exc import DBAPIError




# @view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
# def my_view(request):
#     try:
#         query = request.dbsession.query(MyModel)
#         one = query.filter(MyModel.name == 'one').first()
#     except DBAPIError:
#         return Response(db_err_msg, content_type='text/plain', status=500)
#     return {'one': one, 'project': 'lj-step3'}


# @view_config(route_name='edit', renderer="../templates/edit-model.jinja2")
# def edit_view(request):
#     import pdb;pdb.set_trace()
#     data = {"name": "A new form"}
#     if request.method == "POST":
#         data["name"] = request.POST["name"]

#     return {"data": data}


