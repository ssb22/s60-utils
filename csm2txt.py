#!/usr/bin/env python2

# .csm (PIMBackup Messages dump) to .txt
# Silas S. Brown 2018 - public domain

ignore = [
    # Customise this - headers to ignore
    "Msg Id",
    "BodyType",
    "Folder",
    "Account",
    "Msg Class",
    "Msg Size",
    "Msg Flags",
    "Msg Status",
    "Recipient Nbr",
    "Attachment Nbr",
    "Content Length",
]

import csv
from cStringIO import StringIO
class csm(csv.excel):
    delimiter = ';'
    doublequote = False
csv.register_dialect("csm",csm)
headers = []
for r in csv.reader(StringIO(open("msgs.csm").read().decode('utf-16').encode('utf-8')),"csm"):
    if headers:
        for k,v in zip(headers,r):
            if k in ignore: continue
            if k.endswith("Time"):
                try: y,m,d,h,mm,s = v.split(",")
                except: continue # no time ?
                v = "%s-%s-%s %s:%s:%s" % (y,m,d,h,mm,s)
            if v: print k+":",v
        print
    else: headers = r
