import os
import sqlite3
import time
import sys

import collections

Fortune = collections.namedtuple('Fortune',
        ['created', 'quote', 'author', 'submitter'])

class FortuneCatDB(object):
    def __init__(self, path):
        super(FortuneCatDB, self).__init__()
        if not os.path.exists(path):
            raise StandardError("Database not found")
        self._conn = sqlite3.connect(path)

    def all_quotes(self):
        cursor = self._conn.cursor()
        return [ Fortune(*x) for x in cursor.execute("SELECT * FROM quips") ]

    def random_quote(self):
        q = self._conn.execute("SELECT * FROM quips ORDER BY RANDOM() LIMIT 1")
        return Fortune(*q.fetchone())

    def add_quote(self, quote, author, submitter):
        if quote is None or len(quote.strip()) == 0:
            raise StandardError("Quote may not be empty!")
        if author is None or len(author.strip()) == 0:
            raise StandardError("Author may not be empty!")
        if submitter is None or len(submitter.strip()) == 0:
            raise StandardError("Submitter may not be empty!")
        cursor = self._conn.cursor()
        cursor.execute(
                "INSERT INTO quips VALUES (?, ?, ?, ?)",
                (int(time.time()), quote, author, submitter))
        self._conn.commit()

    @staticmethod
    def create_db(path):
        if os.path.exists(path):
            raise StandardError("Database already exists")
        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE quips(
                created INTEGER(8),
                quote TEXT,
                author TEXT,
                submitter TEXT)""")



if __name__ == "__main__":
    db_path = sys.argv[1]
    if not os.path.exists(db_path):
        FortuneCatDB.create_db(db_path)
    db = FortuneCatDB(db_path)
    while True:
        data = raw_input('qt: ')
        if len(data) == 0:
            break
        db.add_quote(data, 'dfrice', 'dfrice')

    print "Done. Current contents of database:"

    for x in db.all_quotes():
        print "%r" % (x, )

    print "Random quote 1:"
    print "%r" % (db.random_quote(), )
    print "Random quote 2:"
    print "%r" % (db.random_quote(), )
