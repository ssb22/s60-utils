
# Simple S60 stopwatch - Silas S. Brown 2010 - Public Domain - no warranty

# Limitations: You can't set the font, and it's very small.
# (I can't get appuifw's font commands to work on my device.)

# Where to find history:
# on GitHub at https://github.com/ssb22/s60-utils
# and on GitLab at https://gitlab.com/ssb22/s60-utils
# and on BitBucket https://bitbucket.org/ssb22/s60-utils

import appuifw, e32, time, keycapture, key_codes

def sleepto(endtime):
    while time.time()<endtime: e32.ao_sleep(min(0.1,endtime-time.time()))

def printtime():
    if stopped: secs = stopped
    elif startTime: secs = time.time()-startTime
    else: secs = 0
    t = appuifw.Text(u"%d:%02d:%02d\nRight softkey is start/stop/reset (sorry about wrong label)" % (int(secs/3600),int(secs/60)%60,int(secs)%60))
    t.color,t.focus,t.style = (0,0,0),False,appuifw.STYLE_BOLD # might have no effect
    appuifw.app.body = t

needquit=0
def quit():
    global needquit ; needquit=1
appuifw.app.menu=[(u"Exit",quit)]

def start():
    global startTime ; startTime = time.time()
    appuifw.app.exit_key_handler = stop

def stop():
    global stopped ; stopped=time.time()-startTime
    appuifw.app.exit_key_handler = reset

def reset():
    global startTime,stopped ; startTime=stopped=0
    appuifw.app.exit_key_handler = start

appuifw.app.exit_key_handler = quit

reset()
nextSec = 0
while not needquit:
    printtime()
    if nextSec and startTime:
        nextSec += 1 ; sleepto(startTime+nextSec)
    elif startTime:
        nextSec = 1 ; sleepto(startTime+nextSec)
    else:
        nextSec = 0 ; e32.ao_sleep(0.3)

appuifw.app.set_exit()
