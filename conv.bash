#!/bin/bash
cd $(dirname $0)

SRCDIR=./orig
DSTDIR=./conv

remove_unneeded() {
  mkdir -p "$DSTDIR"
  for f in $(find $DSTDIR -type f); do
    fn="${f#$DSTDIR/}"
    if [ ! -f "$SRCDIR/$fn" ]; then
      echo "removing $fn"
      sleep 1
      rm -f "$f"
    fi
  done
}

process_files() {
  for f in $(find $SRCDIR -type f); do
    fn="${f#$SRCDIR/}"
    d="$DSTDIR/$fn"

    if [ "$f" -nt "$DSTDIR/$fn" ]; then
      mkdir -p "$DSTDIR/$(dirname "$fn")"
      echo "$f" #"$DSTDIR/$fn"

      if showttf "$f" | grep -q 'Bitmap Image Size'; then
        python removebitmap.py "$f" "$d"
      else
        cp "$f" "$d"
      fi
    fi
  done
}

remove_unneeded
process_files
