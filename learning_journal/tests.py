# import pytest


# from pyramid import testing


# def test_detail_view():
#     '''Checks respons to reques with id 13 contains a title'''
#     from .views import detail_view
#     request = testing.DummyRequest()
#     request.matchdict['id'] = 13
#     info = detail_view(request)
#     assert "title" in info


# @pytest.fixture()
# def testapp():
#     '''makes test app for testing'''
#     from learning_journal import main
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
