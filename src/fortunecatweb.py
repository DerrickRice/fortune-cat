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
    if f.author is None or f.author.lower() == "none" or len(f.author) == 0:
        return "%s" % (f.quote, )
    else:
        return "%s\n\n  -- %s" % (f.quote, f.author)

@bottle.route('/fortune/all')
def fortune_all():
    f = FortuneCatDB(DB_PATH).all_quotes()
    return bottle.template('fortune_all', fortunes=f)

@bottle.route('/fortune/add')
def fortune_add():
    """ Renders the page / form for adding a new fortune """
    return bottle.template('fortune_add')

def reflow(content):
    import textwrap, re

    def replace_content(content):
        if len(content) == 0 or content.isspace():
            return content
        else:
            return textwrap.fill(content, 32)

    return "".join([ replace_content(x) for x in re.split(r'(\n\s*\n)', content) ])

@bottle.post('/fortune/submit')
def fortune_submit():
    """ Where POST requests land with the new fortunes to add """
    content = bottle.request.forms.get('content')
    author = bottle.request.forms.get('author')
    submitter = bottle.request.forms.get('submitter')
    tags = bottle.request.forms.get('tags')
    do_reflow = bottle.request.forms.get('reflow')

    if '@' in submitter:
        submitter = submitter[:submitter.index('@')]

    error = None
    try:
        if do_reflow:
            content = reflow(content)
        elif ([ x for x in content.split('\n') if len(x) > 32 ]):
            raise StandardError("You have a line longer than 32 and asked for no reflow!")
        FortuneCatDB(DB_PATH).add_quote(content, author, submitter, tags)
    except Exception, err:
        error = err

    return bottle.template('fortune_submit', error=error)

if __name__ == "__main__":
    bottle.run(host='::', port=8081)

