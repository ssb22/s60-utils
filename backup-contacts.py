
# S60 contacts backup - Silas S. Brown 2010 - Public Domain - no warranty

# Where to find history:
# on GitHub at https://github.com/ssb22/s60-utils
# and on GitLab at https://gitlab.com/ssb22/s60-utils
# and on BitBucket https://bitbucket.org/ssb22/s60-utils
# and at https://gitlab.developers.cam.ac.uk/ssb22/s60-utils
# and in China https://gitee.com/ssb22/s60-utils

file_to_write = r"E:\contacts-backup.txt" # or .vcf if you like

import contacts
cdb = contacts.open()
print "Writing",len(cdb),"vcards to",file_to_write
open(file_to_write,"w").write(cdb.export_vcards(tuple(cdb.keys())))
print "Done"
