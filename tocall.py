
# S60 To-Call List (c) 2010 Silas S. Brown.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# If in the European Union, you must comply with the 2018 General Data
# Protection Regulation (GDPR) and not keep written notes about any person
# who has not given you permission to do so.  Although the GDPR supposedly
# grants exemption to "personal or household activities", preliminary
# ruling C-25/17 point 21 implies that an individual doing something as
# innocuous as recommending their club, if it causes people to THINK this
# amounts to working for the club, could be breaking the law by using a notes file.

read_from = r"E:\tocall.txt" # save your notes there

max_matches = 4 # if more than this number of contacts match a name, don't link it

import contacts, re, time, e32
items = open(read_from).read() # will crash if not exist
htmlFilename = r"E:\tocall.html"
cdb = contacts.open()
count = 0 ; htmlFile=open(htmlFilename,"w")
htmlFile.write("<HTML><BODY>")
conNotes = {}
for item in items.split("\n"):
    if not item: continue
    count += 1 ; print "Importing item",count
    e32.ao_sleep(0.1) # allow display to refresh
    item = item.replace("&","@&&@").replace("<","@<<@")
    def myfunc(m):
        word = item[m.start():m.end()]
        if not word: return word
        if not word in conNotes:
            notes = []
            cons = cdb.find(u""+word)
            if len(cons) <= max_matches:
              for con in cons:
                thisCon = []
                for val in [field.value for field in con.find()]:
                    if val=="private": continue
                    if re.match("^[0-9+]*$",val): val="<A HREF=\"tel:"+val+"\">"+val+"</A>"
                    else: val=re.sub("(?i)"+word,"<EM>"+word+"</EM>",val,1)
                    thisCon.append(val)
                notes.append(" ".join(thisCon))
            if notes:
                conNotes[word]=";<BR>".join(notes)
                htmlFile.write("<A NAME=\"_"+word+"\"></A>")
            else: conNotes[word] = None
        if conNotes[word]: return "<A HREF=\"#"+word+"\">"+word+"</A>"
        else: return word
    htmlFile.write(re.sub(r"(\+?[0-9 ]{8,16})",r'<A HREF="tel:\1">\1</A>',re.sub("[A-Za-z]*",myfunc,item)).replace("@&&@","&amp;").replace("@<<@","&lt;")+"<HR>")
print "Writing contacts" ; e32.ao_sleep(0.1)
if filter(lambda x:x,conNotes.values()): htmlFile.write("<H1>End of notes. Contacts:</H1>")
for word,notes in conNotes.items():
    if notes: htmlFile.write("<A NAME=\""+word+"\"></A><A HREF=\"#_"+word+"\">"+word+"</A>: "+notes+"<HR>")

print "Done (wrote",count,"items)"
htmlFile.write("</UL></BODY></HTML>")
htmlFile.close()
try: e32.start_exe(r"z:\system\programs\apprun.exe", r"z:\System\Apps\Browser\Browser.app file://"+htmlFilename, 1)
except: print "Please open",htmlFilename
