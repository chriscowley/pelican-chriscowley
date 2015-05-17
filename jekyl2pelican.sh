#!/bin/bash

input=$1
outdir="content"
#tail -n +2 $infile | egrep -v "date:" | sed -e 's/^---//'

function convert_file() {
  infile=$1
  outfile="${outdir}/$(basename $file | sed 's/.markdown$/.md/')"
  sed -e '/---/d' -e 's/categories:/category:/g' \
      -e '/layout: /d' \
      -e '/permalink\:/s/\.html//g' -e '/permalink:/s/permalink:/Slug:/g' \
      -e 's/Slug: \//Slug: /g' -e 's/&#8217;/''/g' $infile > $outfile
  echo $infile $outfile
}

if [ -d ${input} ]
then
    echo "input is a directory"
    for file in `ls ${input}/*.markdown`
    do
        convert_file ${file}
    done
else
    echo "input is a file"a
    file=${input}
    convert_file ${file}
fi
