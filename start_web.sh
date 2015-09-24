#!/bin/bash -e

function usage() {
  echo "Usage: $0 <VARDIR>"
}

THIS_DIR=$(dirname "$(readlink -f "$0")")
WEBSERVER="$THIS_DIR"/src/fortunecatweb.py

if [ -z "$1" ]; then
  usage >&2
  exit 1
fi

VARDIR="$1"

if [ ! -f "$VARDIR/quotes.sqlite3" ]; then
  echo "Unable to find 'quotes.sqlite3' in $VARDIR" >&2
  echo "To create, run the following:" >&2
  echo "    python $THIS_DIR/src/fortunecatdb.py $VARDIR/quotes.sqlite3" >&2
  exit 1
fi

ACCLOG="$VARDIR/access.log"
ERRLOG="$VARDIR/error.log"

echo "Starting webserver in the background..."
echo "	Access logs to $ACCLOG"
echo "	Error logs to $ERRLOG"

python "$WEBSERVER" "$VARDIR/quotes.sqlite3" > "$ACCLOG" 2> "$ERRLOG" &

echo "Started. PID= $!"
echo "	disowning..."
disown $!
echo "Done! You may disconnect."
