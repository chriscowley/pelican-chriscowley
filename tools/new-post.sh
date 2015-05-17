#!/bin/sh

TITLE=$1
SLUG=$(echo ${TITLE} | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g')
DATE=$(date +%Y-%m-%d)
echo "${TITLE}"
echo "########"
echo
echo ":slug: ${SLUG}"
echo ":date: ${DATE}"
echo ":category:"
echo ":tags:"
echo ":summary:"
echo ":authors:"
echo
