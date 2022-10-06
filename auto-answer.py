# S60 auto-answer script for meetings dail-in

# Silas S. Brown 2010 - Public Domain - no warranty

# Note: This script can auto-answer only ONE call at a time.
# If a second call comes in on call waiting, it is ignored
# (call_state does not tell us unless you manually answer first,
# and even then we have no way to automatically conference it).
# But if the 1st caller hangs up, this script can answer again.

# (NB also that Exit won't work if we're waiting
# to send an SMS.  Would need to long-press Menu
# to get task manager and exit from there.)

# Where to find history:
# on GitHub at https://github.com/ssb22/s60-utils
# and on GitLab at https://gitlab.com/ssb22/s60-utils
# and on BitBucket https://bitbucket.org/ssb22/s60-utils
# and at https://gitlab.developers.cam.ac.uk/ssb22/s60-utils
# and in China: https://gitee.com/ssb22/s60-utils

name = ""
textNo = ""
textMsg = ""
meeting_start_time = (12,00)
# If you set the above, the program can offer to
# text someone, e.g.:
# name = "Bob"
# textNo = "01234567890"
# textMsg = "The meeting has started - call me"
# meeting_start_time = (11,30) # note 24hr clock

import appuifw,e32,telephone,time,messaging

def quit(): app_lock.signal()
appuifw.app.exit_key_handler = quit
app_lock=e32.Ao_lock()

def stateChange((callState, number)):
    print "%d:%02d" % time.localtime()[3:5],"callState",callState
    if callState == telephone.EStatusRinging:
      if number == "": print "incoming call"
      else: print "call from "+number
      telephone.incoming_call()
      e32.ao_sleep(1)
      telephone.answer()
      e32.ao_sleep(1)
      global got_call ; got_call = True

got_call = False
telephone.call_state(stateChange)

print "Waiting for a call"

if meeting_start_time: h,m = meeting_start_time
else: h=m=None
if h and textNo and appuifw.query(u"Text %s at %d:%d if no calls?" % (name,h,m),'query'):
  while time.localtime()[3:5] < (h,m): e32.ao_sleep(1)
  if got_call: print "Not SMS'ing as got a call"
  else:
    print "Sending SMS to",textNo
    messaging.sms_send(textNo,textMsg)

app_lock.wait()
print "Exit pressed: script finished."
