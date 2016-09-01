import os
import sys
import transaction
import datetime

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )

from ..models import Entry


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        entry1 = Entry(title="James Tuesday week 3", date=datetime.datetime.strptime('August 22, 2016', '%B %d, %Y'), body="<p>As my partner and I were planning how to do a min-heap we could not think of any cases where simply having a list ordered from smallest to largest would be wrong. We figured a heap is just a list of values, there is no actual pyramid shaped thing with nodes and children, that is just an imaginary visualization to help understand it. It's a just a list and if all the values in the list are in order then they can fit into that pyramid, nodes with children structure fine.</p><p>It works according to duck types (it acts like a heap) and the zen of python says it's better to ask forgiveness than permission.</p><p>Not really in the mood to learn pyramid as I dont think I will use it after this course...</p>")
        entry2 = Entry(title="James Monday week 3", date=datetime.datetime.strptime('August 23, 2016', '%B %d, %Y'), body="<p>Today I leant about pyramid and deploying pyramid on Heroku. It's pretty bad. Of the platforms and deployment parings I have tried its most similar to deploying laravel on a VPS (but that can be made much easier by using forge managed Laravel platform). Deploying JS apps on Heroku is easier and you get single page architecture. Deploying Wordpress on managed hosting is 100 times easier and you get a lot of advantages.</p><p> I am not particularly looking forward to learning about pyramid but I do look forward to some forced SQL practice.")
        entry3 = Entry(title="James Friday week 2", date=datetime.datetime.strptime('August 24, 2016', '%B %d, %Y'), body="<p>Code challenge was fine, I am generally okay with string manipulation as long as I have google.</p><p>Whiteboarding, it was good to code using a slightly different part of my brain than normal (hand writing instead of typing) . I dont really get the task. We thought we were given a linked list of nodes and that made some sense but then it turned out to be a single node (bag of nodes was also mentioned, or was it 1 node from a bag of nodes?) So if the function gets one node how are there potentially multiple nodes to traverse? Whatevs.</p><p>I am pretty lost in the server assignment, one night my partner worked on it and made a new class in a separate module for...requests I think, it's probably a fine idea but somehow we are returning 2 replies for 1 request and I lost the flow of the messages back and forth through the code.</p><p>Had an interesting moment when a TA seemed to suggest the code does not need to work in a terminal as long as the tests pass, I disagree, our test only test individual functions not how the functions interact with each other or the server as a whole. By about 5 my partner was brain fried so we called it a day half way through step 3...</p>")
        entry4 = Entry(title="James Thursday week 2", date=datetime.datetime.strptime('August 25, 2016', '%B %d, %Y'), body="<p>All week I have understood very little of the lectures. I would understand more if more topics had a little follow long by coding task and if the time we could/should follow along by coding were more spoon fed, like - 'okay everyone now we are going to follow along by coding, open a terminal and run python 3'</p><p>'Now do xyz, is everyone up to here?' (dont go on unless everyone is up to there)</p><p>'Now try abc...'</p><p> and so on and so forth rather than keep up if you can.</p>")
        dbsession.add(entry1)
        dbsession.add(entry2)
        dbsession.add(entry3)
        dbsession.add(entry4)

