#!/bin/bash
set -e

cd $(dirname $0)

SRCDIR=./orig
DSTDIR=./conv

process_files() {
  for f in $(find $SRCDIR -type f); do
    fn="${f#$SRCDIR/}"
    d="$DSTDIR/$fn"
    needconv=0

    ext="${fn##*.}"
    if [[ $ext == "fon" ]]; then
      # skip: not supported by fontforge
      continue
    elif [[ $ext == "dfont" ]]; then
      # convert to ttf
      needconv=1
      d="${d%.*}.ttf"
    fi

    if [ "$f" -nt $d ]; then
      mkdir -p "$DSTDIR/$(dirname "$fn")"
      echo "$f"

      if showttf "$f" | grep -q 'Bitmap Image Size'; then
        needconv=1
      fi
      if [[ $needconv == 1 ]]; then
        python removebitmap.py "$f" "$d"
      else
        cp "$f" "$d"
      fi
    fi
  done
}

process_files
