#!/bin/bash
wget -N http://people.ds.cam.ac.uk/ssb22/s60/auto-answer.py
wget -N http://people.ds.cam.ac.uk/ssb22/s60/backup-contacts.py
wget -N http://people.ds.cam.ac.uk/ssb22/s60/backup-inbox.py
wget -N http://people.ds.cam.ac.uk/ssb22/s60/cleanup.py
wget -N http://people.ds.cam.ac.uk/ssb22/s60/contacts2csc.py
wget -N http://people.ds.cam.ac.uk/ssb22/s60/csc2vcf.py
wget -N http://people.ds.cam.ac.uk/ssb22/s60/list-cdrive.py
wget -N http://people.ds.cam.ac.uk/ssb22/s60/restore-contacts.py
git commit -am update && git push