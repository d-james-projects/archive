#!/bin/bash
filename=$1
dest=$2
while read line; do
# reading each line
  echo "[-] reading from file $line"
  g=$(basename "$line")
# g="${line##*/}"
  echo "got name $g"
  rm -rf /tmp/temp.git
  git clone --bare "$line" /tmp/temp.git
  mv -f /tmp/temp.git "$dest"/"$g"
done < "$filename"

