
# Delete S60 downloads and cache
# Silas S. Brown 2010, public domain, no warranty

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
