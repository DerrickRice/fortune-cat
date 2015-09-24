import os
import sqlite3
import time
import sys

import collections

Fortune = collections.namedtuple('Fortune',
        ['id', 'created', 'quote', 'author', 'submitter', 'tags'])

class FortuneCatDB(object):
    def __init__(self, path):
        super(FortuneCatDB, self).__init__()
        if not os.path.exists(path):
            raise StandardError("Database not found")
        self._conn = sqlite3.connect(path)

    def all_quotes(self):
        cursor = self._conn.cursor()
        return [ Fortune(*x) for x in cursor.execute(
            "SELECT id, created, quote, author, submitter, tags FROM fortunes") ]

    def random_quote(self):
        q = self._conn.execute(
            "SELECT id, created, quote, author, submitter, tags FROM fortunes ORDER BY RANDOM() LIMIT 1")
        x = q.fetchone()
        if x is None:
            return None
        else:
            return Fortune(*x)

    def add_quote(self, quote, author, submitter, tags):
        if quote is None or len(quote.strip()) == 0:
            raise StandardError("Quote may not be empty!")
        if submitter is None or len(submitter.strip()) == 0:
            raise StandardError("Submitter may not be empty!")
        cursor = self._conn.cursor()
        cursor.execute(
                "INSERT INTO fortunes (created, quote, author, submitter, tags) VALUES (?, ?, ?, ?, ?)",
                (int(time.time()), quote, author, submitter, tags))
        self._conn.commit()

    @staticmethod
    def create_db(path):
        if os.path.exists(path):
            raise StandardError("Database already exists")
        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE fortunes(
                id INTEGER PRIMARY KEY,
                created INTEGER(8),
                quote TEXT,
                author TEXT,
                submitter TEXT,
                tags TEXT)""")
            conn.commit()

if __name__ == "__main__":
    db_path = sys.argv[1]
    if os.path.exists(db_path):
        print "Database already exists."
    else:
        FortuneCatDB.create_db(db_path)
        print "Database created."
