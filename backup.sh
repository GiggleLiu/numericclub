#!/bin/bash
# add this file to schedule using `crontab -e`
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cp $DIR/db.sqlite3 $DIR/backup/db.sqlite3.$(date +"%Y-%m-%d")
