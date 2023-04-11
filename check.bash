#!/bin/bash

function check() {
  if showttf $1 2>/dev/null | grep 'Bitmap Image Size' -q; then
    echo "$1"
  fi
}

for arg in "$@"; do
   ((i=i%8)); ((i++==0)) && wait
  check "$arg" # &
done



# wait
