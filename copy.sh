#!/bin/bash
filename=${1:-list.txt}
dest=${2:-/tmp}
set -e
while read line; do
# reading each line
  #echo "[-] reading line $line"
  g=$(basename "$line")
  if [ "$g" = "" ]; then break; fi 
  echo -n "[-] copy $g to $dest"
  cp -r -n "$g" "$dest"
  echo " ...done"
done < "$filename"
