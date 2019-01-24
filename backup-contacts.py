
# S60 contacts backup - Silas S. Brown 2010 - Public Domain - no warranty

file_to_write = r"E:\contacts-backup.txt" # or .vcf if you like

import contacts
cdb = contacts.open()
print "Writing",len(cdb),"vcards to",file_to_write
open(file_to_write,"w").write(cdb.export_vcards(tuple(cdb.keys())))
print "Done"
