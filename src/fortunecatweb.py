import bottle
from fortunecatdb import FortuneCatDB
import os
import sys
import sqlite3

def get_view_dir():
    this_file = os.path.realpath(__file__)
    parent_dir = os.path.dirname(os.path.dirname(this_file))
    return os.path.join(parent_dir, 'views')

bottle.TEMPLATE_PATH = [ get_view_dir() ]
database = None # set later, in main.

def get_db():
    return FortuneCatDB(database)

@bottle.route('/fortune')
def fortune_home():
    return fortune_all()

@bottle.route('/fortune/')
def fortune_home2():
    return fortune_all()

@bottle.route('/fortune/random')
def fortune_random():
    bottle.response.content_type = 'text/plain; charset=utf-8'
    f = get_db().random_quote()
    if f.author is None or f.author.lower() == "none" or len(f.author) == 0:
        return "%s" % (f.quote, )
    else:
        return "%s\n\n  -- %s" % (f.quote, f.author)

@bottle.route('/fortune/all')
def fortune_all():
    f = get_db().all_quotes()
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
        get_db().add_quote(content, author, submitter, tags)
    except Exception, err:
        error = err

    return bottle.template('fortune_submit', error=error)

@bottle.get('/fortune/slurp')
def fortune_slurp():
    import shutil, time, glob, re
    now = int(time.time())
    # retire = now - 60*5 # 5 minutes ago
    retire = now - 5 # 5 seconds ago

    dbdir = os.path.dirname(database)
    dbname = os.path.basename(database)

    # Delete old backups
    prefix = "%s.bak." % (dbname, )
    prefix_len = len(prefix)
    for fname in os.listdir(dbdir):
        full_fname = os.path.join(dbdir, fname)
        if not fname.startswith(prefix):
            continue
        try:
            ts = int(fname[prefix_len:])
            if ts < retire:
                os.remove(full_fname)
        except ValueError, err:
            continue

    with sqlite3.connect(database) as conn:
        # locked...
        new_name = "%s.bak.%d" % (dbname, int(time.time()))
        shutil.copy(database, os.path.join(dbdir, new_name))

    return bottle.static_file(new_name, os.path.abspath(dbdir), download=dbname)

if __name__ == "__main__":
    database = sys.argv[1]
    bottle.run(host='::', port=8081)

