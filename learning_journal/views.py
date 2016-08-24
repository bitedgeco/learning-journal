from pyramid.response import Response
import os


def includeme(config):
    config.add_view(home, route_name='home')
    config.add_view(detail, route_name='detail')
    config.add_view(edit, route_name='edit')
    config.add_view(new, route_name='new')


HERE = os.path.dirname(__file__)


def home(request):
    imported_text = open(os.path.join(HERE, 'templates/home.html')).read()
    return Response(imported_text)


def detail(request):
    imported_text = open(os.path.join(HERE, 'templates/detail.html')).read()
    return Response(imported_text)


def edit(request):
    imported_text = open(os.path.join(HERE, 'templates/edit.html')).read()
    return Response(imported_text)


def new(request):
    imported_text = open(os.path.join(HERE, 'templates/new.html')).read()
    return Response(imported_text)
