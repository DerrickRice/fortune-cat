from bottle import route, run, template
from fortunecatdb import FortuneCatDB

DB_PATH = '/tmp/dfrice.sqlite3'

@route('/fortune')
def get_fortune():
    f = FortuneCatDB(DB_PATH).random_quote()
    return "%s\n\n  -- %s" % (f.quote, f.author)

run(port=8081)

