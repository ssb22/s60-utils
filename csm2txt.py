#!/usr/bin/env python2

# .csm (PIMBackup Messages dump) to .txt
# Silas S. Brown 2018 - public domain

indent = 16

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
    escapechar = "\\"
    quoting = csv.QUOTE_NONE
    doublequote = False
def escape_newlines(s):
    inBody = False ; o = []
    for l in s.split("\n"):
        numQuotes=max(0,len(l.replace('\\"','').split('"'))-1)
        if numQuotes % 2: inBody = not inBody
        if inBody: o.append(l+r"\\n"+" "*indent)
        else: o.append(l+"\n")
    return "".join(o)
csv.register_dialect("csm",csm)
headers = [] ; out = []
for r in csv.reader(StringIO(escape_newlines(open("msgs.csm").read().decode('utf-16').encode('utf-8').replace("\r\n","\n"))),"csm"):
    if headers:
        row = [] ; tt = None
        for k,v in zip(headers,r):
            if v.startswith('"') and v.endswith('"'):
                v=v[1:-1]
            if k in ignore: continue
            if k.endswith("Time"):
                try: y,m,d,h,mm,s = v.split(",")
                except: continue # no time ?
                tt=v="%s-%s-%s %s:%s:%s" % (y,m,d,h,mm,s)
            if v: row.append(k+":"+" "*max(1,indent-1-len(k))+v.replace(r"\n","\n"))
        if row: out.append((tt,"\n".join(row)))
    else: headers = r
print "\n\n".join(o for _,o in sorted(out))
