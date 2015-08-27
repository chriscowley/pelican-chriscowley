#!/bin/sh

TITLE=$1
SLUG=$(echo ${TITLE} | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g')
DATE=$(date +%Y-%m-%d)
n=${#TITLE}
echo "${TITLE}"
for ((i=0;i<n; i++)) {
    echo -n "#"
}
printf "\n\n"
echo ":slug: ${SLUG}"
echo ":category:"
echo ":tags:"
echo ":summary:"
echo ":status: draft"
echo ":authors:"
echo 
