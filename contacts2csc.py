
# S60 contacts to WM PIMBackup file - Silas S. Brown 2011 - public domain - no warranty

# This script is ASCII-only for now; PIM Backup can also take UTF-16.

# Where to find history:
# on GitHub at https://github.com/ssb22/s60-utils
# and on GitLab at https://gitlab.com/ssb22/s60-utils
# and on BitBucket https://bitbucket.org/ssb22/s60-utils
# and at https://gitlab.developers.cam.ac.uk/ssb22/s60-utils
# and in China: git clone https://gitee.com/ssb22/s60-utils

file_to_write = r"E:\contacts.csc"

cscFields="Name;Title;First Name;Middle Name;Last Name;NickName;Suffix;Display Name;Picture;Job Title;Department;Company;Business Phone;Business Fax;Business Street;Business City;Business State;Business Postal Code;Business Country;IM;E-mail Address;Mobile Phone;Ring Tone;Web Page;Office Location;Home Phone;Home Street;Home City;Home State;Home Postal Code;Home Country;Categories;Other Street;Other City;Other State;Other Postal Code;Other Country;Pager;Car Phone;Home Fax;Company Main Phone;Business Phone 2;Home Phone 2;Radio Phone;IM2;IM3;E-mail 2 Address;E-mail 3 Address;Assistant's Name;Assistant's Phone;Manager's Name;Government ID Number;Account;Customer ID Number;Birthday;Anniversary;Spouse;Children;Notes;Notes Ink;Last Name (Yomi);First Name (Yomi);Company (Yomi)"
o=open(file_to_write,"w") ; o.write(cscFields+"\n")
cscFields=cscFields.lower().split(";")
class CscField:
  def __init__(self): self.vals=[""]*len(cscFields)
  def resolveKey(self,k,location):
    oldK = k
    if location=="work": location="business "
    elif location=="home": location="home "
    elif location=="none": location=""
    else:
      print "Warning: unknown location",repr(location)
      location = ""
    k=k.lower() ; k={"company_name":"company","email_address":"e-mail address","fax_number":"fax","url":"web page","street_address":"street","note":"notes"}.get(k,k).replace("_"," ")
    if k.endswith(" number"): k="phone"
    if location+k in cscFields: return self.rk2(location+k,k=="phone")
    elif k=="phone": return self.rk2("mobile phone",True)
    elif k in cscFields: return self.rk2(k,False)
    print "Warning: unrecognised field",repr(oldK)
  def rk2(self,k,isPhone):
    if isPhone and self.vals[cscFields.index(k)]: # find another phone field
      for i in xrange(len(cscFields)):
        if not self.vals[i] and cscFields[i].endswith("phone"): return i
      print "Warning: too many phone numbers in one contact"
    else: return cscFields.index(k)
  def add(self,k,val,location="none"):
    if k=="unknown" and val==u"private": return # ignore
    i=self.resolveKey(k,location)
    if i==None: print "Losing:",repr(val)
    else: self.vals[i]=val
  def out(self): o.write(";".join(['"'+f.replace('"',"'")+'"' for f in self.vals])+"\n")

import contacts
db=contacts.open()
for i in db:
  f=CscField() ; f.add("name",db[i].title)
  for ff in db[i].find(): f.add(ff.type,ff.value,ff.location)
  f.out()

print "Done to",file_to_write
