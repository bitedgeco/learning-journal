from pyramid.view import view_config

DETAIL = {
    "title": "LJ - Day 12",
    "creation_date": "Aug 23, 2016",
    "body": "Sample body text."
}

ENTRIES = [
    {"title": "James Thursday week 2", "creation_date": "Aug 20, 2016", "id": 10, "body": "<p>As my partner and I were planning how to do a min-heap we could not think of any cases where simply having a list ordered from smallest to largest would be wrong. We figured a heap is just a list of values, there is no actual pyramid shaped thing with nodes and children, that is just an imaginary visualization to help understand it. It's a just a list and if all the values in the list are in order then they can fit into that pyramid, nodes with children structure fine.</p><p>It works according to duck types (it acts like a heap) and the zen of python says it's better to ask forgiveness than permission.</p><p>Not really in the mood to learn pyramid as I dont think I will use it after this course...</p>"},
    {"title": "James Friday  week 2", "creation_date": "Aug 21, 2016", "id": 11, "body": "Sample body text."},
    {"title": "James Monday  week 3", "creation_date": "Aug 22, 2016", "id": 12, "body": "Sample body text."},
    {"title": "James Tuesday  week 3", "creation_date": "Aug 23, 2016", "id": 13, "body": "Sample body text."},
]


@view_config(route_name='home', renderer='templates/home.jinja2')
def home_view(request):
    return {"entries": ENTRIES}


@view_config(route_name='detail', renderer='templates/detail.jinja2')
def detail_view(request):
    return ENTRIES[0]


@view_config(route_name='edit', renderer='templates/edit.jinja2')
def edit_view(request):
    return {"entries": ENTRIES}


@view_config(route_name='new', renderer='templates/new.jinja2')
def new_list_view(request):
    return {"entries": ENTRIES}
