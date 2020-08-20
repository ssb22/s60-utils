
# S60 contacts restore - Silas S. Brown 2010 - Public Domain - no warranty

# Where to find history:
# on GitHub at https://github.com/ssb22/s60-utils
# and on GitLab at https://gitlab.com/ssb22/s60-utils
# and on BitBucket https://bitbucket.org/ssb22/s60-utils
# and at https://gitlab.developers.cam.ac.uk/ssb22/s60-utils

file_to_read = r"E:\contacts-backup.txt"

import contacts
print "Reading",file_to_read
contacts.open().import_vcards(open(file_to_read).read())
print "Done"
