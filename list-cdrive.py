
# List the files on S60 C drive, including
# some folders not shown by the file manager
# (but not SYS and PRIVATE unfortunately).
# Output is written to list.txt on the memory card.

# Silas S. Brown 2010, public domain, no warranty

# Where to find history:
# on GitHub at https://github.com/ssb22/s60-utils
# and on GitLab at https://gitlab.com/ssb22/s60-utils
# and on BitBucket https://bitbucket.org/ssb22/s60-utils

import os,os.path,time
def timestr(t):
    n=time.time()
    t2=time.localtime(t)
    if t>n-24*3600: return "%02d:%02d" % t2[3:5]
    elif t>n-365*24*3600: return "%d-%02d" % t2[1:3]
    else: return "%04d" % t2[0]

def listing(d,accum):
    for subdir in os.listdir(d):
        l=len(accum)
        if os.path.isdir(d+subdir): listing(d+subdir+"\\",accum)
        if len(accum)==l:
            try: mt=" ("+timestr(os.stat(d+subdir).st_mtime)+")"
            except: mt="" # permissions error?
            accum.append(d+subdir+mt)
a=[] ; listing("C:\\",a)
open("E:\\list.txt","w").write("\n".join(a).replace("\\","/")) # (/ can be easier to view in S60 notes app)
print "Written to E:\\list.txt"
