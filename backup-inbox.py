
# S60 inbox backup - Silas S. Brown 2011 - Public Domain - no warranty

file_to_write = r"E:\inbox-backup.txt"

import inbox,time
box = inbox.Inbox() # or Inbox(inbox.ESent) for sent-mail
o=open(file_to_write,"w")
for msgid in box.sms_messages(): o.write((box.address(msgid)+": "+box.content(msgid)).encode('utf-8')+' ('+time.asctime(time.localtime(box.time(msgid)))+")\n")
print "Done"
