
# Delete S60 downloads and cache
# Silas S. Brown 2010, public domain, no warranty

# Where to find history:
# on GitHub at https://github.com/ssb22/s60-utils
# and on GitLab at https://gitlab.com/ssb22/s60-utils
# and on BitBucket https://bitbucket.org/ssb22/s60-utils
# and at https://gitlab.developers.cam.ac.uk/ssb22/s60-utils
# and in China: git clone https://gitee.com/ssb22/s60-utils

import os
def myrm(fname):
    try: os.remove(fname)
    except: return
    print "Deleted",fname
myrm(r"C:\SYSTEM\Temp\RtspTemp.ram")
def delall(d):
    try: l=os.listdir(d)
    except: return
    for f in l: myrm(d+"\\"+f)

for dmgr in os.listdir(r"C:\SYSTEM\dmgr"):
    for sd in ["contents","downloads"]: delall("C:\\SYSTEM\\dmgr\\"+dmgr+"\\"+sd)
delall("C:\\cache")
print "Finished"
