#!/bin/bash

input=$1
outdir="content"
#tail -n +2 $infile | egrep -v "date:" | sed -e 's/^---//'

function convert_file() {
  infile=$1
  tempmdfile="/tmp/$(basename $file | sed 's/.markdown$/.md/')"
  outfile="${outdir}/$(basename $file | sed 's/.markdown$/.rst/')"
  contentrstfile="${outdir}/$(basename $file | sed 's/.markdown$/.temp.rst/')"

#  sed -e '/---/d' -e 's/categories:/category:/g' \
#      -e '/layout: /d' \
#      -e '/permalink\:/s/\.html//g' -e '/permalink:/s/permalink:/Slug:/g' \
#      -e 's/Slug: \//Slug: /g' -e 's/&#8217;/''/g' $infile > $outfile
  sed -e 's/{% codeblock %}/\`\`\`/g' -e 's/{% endcodeblock %}/\`\`\`/g' ${infile} > ${tempmdfile}
  pandoc  ${tempmdfile} -o ${contentrstfile}
  title=$(grep -e "^title: " ${tempmdfile}  | cut -d ":" -f 2- | sed 's/^ //' | sed 's/"//g' )
#  category=$(grep -e "^categories: " ${infile}  | cut -d ":" -f 2- | cut -d "'" -f 2 | cut -d "," -f 1)
  tags=$(grep -e "^categories: " ${tempmdfile}  | cut -d ":" -f 2- | cut -d "'" -f 2)
  echo ${title} > temp.$$
  for ((i=1;i<=${#title}; i++))
  do
      echo -n "#"
  done >> temp.$$
  echo >> temp.$$
#  echo ":category: ${category}" >> temp.$$
  echo ":tags: ${tags}" >> temp.$$
  echo >> temp.$$
  cat temp.$$ ${contentrstfile} > ${outfile}
  rm temp.$$ ${contentrstfile} ${tempmdfile}
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
