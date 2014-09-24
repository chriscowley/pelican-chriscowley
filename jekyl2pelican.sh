#!/bin/bash

input=$1
outdir="output"
#tail -n +2 $infile | egrep -v "date:" | sed -e 's/^---//'

function convert_file() {
  outfile="${outdir}/$(basename $file)"
  echo $1 $outfile
}

if [ -d ${input} ]
then
    echo "input is a directory"
    for file in `ls ${input}/*.markdown`
    do
        convert_file ${file}
    done
else
    echo "input is a file"
fi
