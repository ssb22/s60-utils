
# S60 inbox backup - Silas S. Brown 2011 - Public Domain - no warranty

# Where to find history:
# on GitHub at https://github.com/ssb22/s60-utils
# and on GitLab at https://gitlab.com/ssb22/s60-utils
# and on BitBucket https://bitbucket.org/ssb22/s60-utils
# and at https://gitlab.developers.cam.ac.uk/ssb22/s60-utils

file_to_write = r"E:\inbox-backup.txt"

import inbox,time
box = inbox.Inbox() # or Inbox(inbox.ESent) for sent-mail
o=open(file_to_write,"w")
for msgid in box.sms_messages(): o.write((box.address(msgid)+": "+box.content(msgid)).encode('utf-8')+' ('+time.asctime(time.localtime(box.time(msgid)))+")\n")
print "Done"
