from pyramid.response import Response


def home_page(request):
    return Response("This is my first view!")


def includeme(config):
    config.add_view(home_page, route_name='home')
