#!/bin/bash
git pull --no-edit
wget -N http://ssb22.user.srcf.net/s60/auto-answer.py
wget -N http://ssb22.user.srcf.net/s60/backup-contacts.py
wget -N http://ssb22.user.srcf.net/s60/backup-inbox.py
wget -N http://ssb22.user.srcf.net/s60/cleanup.py
wget -N http://ssb22.user.srcf.net/s60/contacts2csc.py
wget -N http://ssb22.user.srcf.net/s60/list-cdrive.py
wget -N http://ssb22.user.srcf.net/s60/restore-contacts.py
wget -N http://ssb22.user.srcf.net/s60/stopwatch.py
wget -N http://ssb22.user.srcf.net/s60/tocall.py
git commit -am update && git push
