import bottle
from fortunecatdb import FortuneCatDB
import os

def get_view_dir():
    this_file = os.path.realpath(__file__)
    parent_dir = os.path.dirname(os.path.dirname(this_file))
    return os.path.join(parent_dir, 'views')

bottle.TEMPLATE_PATH = [ get_view_dir() ]
DB_PATH = '/tmp/dfrice.sqlite3'

@bottle.route('/fortune')
def fortune_home():
    pass

@bottle.route('/fortune/random')
def fortune_random():
    bottle.response.content_type = 'text/plain; charset=utf-8'
    f = FortuneCatDB(DB_PATH).random_quote()
    return "%s\n\n  -- %s" % (f.quote, f.author)

@bottle.route('/fortune/all')
def fortune_all():
    f = FortuneCatDB(DB_PATH).all_quotes()
    return bottle.template('fortune_all', fortunes=f)

@bottle.route('/fortune/add')
def fortune_add():
    """ Renders the page / form for adding a new fortune """
    return bottle.template('fortune_add')

@bottle.post('/fortune/submit')
def fortune_submit():
    """ Where POST requests land with the new fortunes to add """
    content = bottle.request.forms.get('content')
    author = bottle.request.forms.get('author')
    submitter = bottle.request.forms.get('submitter')
    error = None
    try:
        FortuneCatDB(DB_PATH).add_quote(content, author, submitter)
    except Exception, err:
        error = err

    return bottle.template('fortune_submit', error=error)

bottle.run(host='::', port=8081)

