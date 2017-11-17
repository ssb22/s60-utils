
# S60 contacts restore - Silas S. Brown 2010 - Public Domain

file_to_read = r"E:\contacts-backup.txt"

import contacts
print "Reading",file_to_read
contacts.open().import_vcards(open(file_to_read).read())
print "Done"
