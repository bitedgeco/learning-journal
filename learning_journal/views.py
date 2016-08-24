from pyramid.response import Response
import os

# def home_page(request):
#     return Response("This is my first view!")


def includeme(config):
    config.add_view(home_page, route_name='home')


HERE = os.path.dirname(__file__)


def home_page(request):
    imported_text = open(os.path.join(HERE, 'template/home.html')).read()
    return Response(imported_text)
