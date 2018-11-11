#!/usr/bin/env python2

# PIMBackup CSC to VCF VCards conversion
# (for copying contacts from Windows Mobile to S60, Android etc)
# Silas S. Brown 2014, 2016 - v1.3 - public domain

# Android (at least v4.4) built-in Contacts import: if
# non-identical contacts already exist, importing an
# update is likely to create new ones and Link them.
# Not sure there's any way to say "delete all old versions of all these" apart from delete all & start again (which would clear non-phone contacts)

infile  = "contacts.csc"
outfile = "contacts.vcf"

import csv, base64, sys, time, re
o = open(outfile,'wb')
class Dialect(csv.Dialect):
    delimiter=';'
    # the rest is not really needed, but some versions of
    # csv won't run without them:
    quoting = csv.QUOTE_MINIMAL
    quotechar = '"'
    lineterminator = '\n'
csv.register_dialect('csc',Dialect)

cscMap = { "Name":"FN", # = "File as" in WM6 Contacts
           "Title":('N',4,3),
           "First Name":('N',4,1),
           "Middle Name":('N',4,2),
           "Last Name":('N',4,0),
           # NickName
           # Suffix
           "Display Name":None, # = "Name" (NOT "File as"!) in WM6 Contacts
           "Picture":"PHOTO;JPEG;ENCODING=BASE64",
           "Job Title":"TITLE",
           "Department":("ORG",2,1),
           "Company":("ORG",2,0),
           "Business Phone":"TEL;TYPE=work",
           # Business Fax
           "Business Street":("ADR;TYPE=work",7,2),
           "Business City":("ADR;TYPE=work",7,3),
           "Business State":("ADR;TYPE=work",7,4),
           "Business Postal Code":("ADR;TYPE=work",7,5),
           "Business Country":("ADR;TYPE=work",7,6),
           "IM":"IMPP","IM2":"IMPP","IM3":"IMPP", # ? (requires VCard 4.0; propsed in 3.0)
           "E-mail Address":"EMAIL",
           "Mobile Phone":"TEL;TYPE=cell",
           # Ring Tone (usually a Windows pathname)
           "Web Page":"URL",
           "Office Location":"ADR;TYPE=work", # ?
           "Home Phone":"TEL;TYPE=home",
           "Home Street":("ADR;TYPE=home",7,2),
           "Home City":("ADR;TYPE=home",7,3),
           "Home State":("ADR;TYPE=home",7,4),
           "Home Postal Code":("ADR;TYPE=home",7,5),
           "Home Country":("ADR;TYPE=home",7,6),
           "Categories":"CATEGORIES", # doesn't seem to have any effect on Android 4.4 (isn't translated to Groups)
           "Other Street":("ADR;TYPE=other",7,2),
           "Other City":("ADR;TYPE=other",7,3),
           "Other State":("ADR;TYPE=other",7,4),
           "Other Postal Code":("ADR;TYPE=other",7,5),
           "Other Country":("ADR;TYPE=other",7,6),
           "Pager":"TEL;TYPE=cell", # usually used as an 'overspill' if person has too many numbers
           "Car Phone":"TEL;TYPE=cell", # ditto
           # Home Fax
           "Company Main Phone":"TEL;TYPE=work",
           "Business Phone 2":"TEL;TYPE=work",
           "Home Phone 2":"TEL;TYPE=home",
           "Radio Phone":"TEL;TYPE=cell", # ditto
           # IM2, IM3 - handled above
           "E-mail 2 Address":"EMAIL",
           "E-mail 3 Address":"EMAIL",
           "Assistant's Name":"X-ASSISTANT",
           "Assistant's Phone":"X-ASSISTANT-TEL",
           # "Manager's Name":"X-MANAGER",
           "Manager's Name":"Note:Manager",
           # Government ID Number
           # Account
           # Customer ID Number
           #"Spouse":"X-SPOUSE", # won't display in Android 4.1
           "Spouse":"NOTE:Spouse",
           "Children":"NOTE:Children",
           "Anniversary":"ANNIVERSARY", # requires VCard 4.0 (and doesn't seem to have any effect in Android 4.4), TODO: put in a NOTE instead?
           "Birthday":"BDAY", # in case date of birth needed for medical purposes?
           "Notes":"NOTE" }

lines = open(infile).read().decode('utf-16').encode('utf-8').replace('\r','').split('\n')
fields = lines[0].split(';')
del lines[0]
for l in csv.reader(lines,'csc'):
    if not l: continue
    assert len(l) == len(fields), len(l)
    o.write("BEGIN:VCARD\r\nVERSION:2.1\r\n")
    warning_id = ""
    extra = {}
    for f,v in zip(fields,l):
        if not v: continue
        try: vd = v.replace("0xfe,0xff,","").replace(",0x00","").replace("0x","\\x").replace(",","").decode('string-escape')
        except: vd = None
        if vd=="<HTCData><!-- Please do not modify -->\r\n<Facebook></Facebook>\r\n</HTCData>\r\n": continue
        if f=="Name": warning_id = " in "+v
        # if f=="Name": sys.stderr.write(v+"\n") # for Info: below
        mapTo = cscMap.get(f,'')
        if mapTo==None: continue
        elif mapTo=='':
            if len(v)<30: f += ': '+v # not e.g. Notes Ink
            sys.stderr.write("Warning: omitting "+f+warning_id+'\n')
            continue
        elif type(mapTo)==tuple:
            if not mapTo[0] in extra:
                extra[mapTo[0]] = ['']*mapTo[1]
            extra[mapTo[0]][mapTo[2]] = v
            continue
       	if f=="Picture":
            v=('\\'+v[1:].replace(',0','\\')).decode('string_escape')
            # from PIL import Image; from cStringIO import StringIO
            # sys.stderr.write("Info: picture size is %dx%d\r\n" % Image.open(StringIO(v)).size)
            v=base64.b64encode(v)+'\r\n' # must leave an extra blank line for Android, otherwise get "File ended during parsing BASE64 binary" - see java/com/android/vcard/VCardParserImpl_V21.java
        else:
            if re.match("^(0x[0-9a-f][0-9a-f],?)*$",v):
                v = v.replace(",","").replace("0x",r"\x").decode("string-escape").decode("utf-16").encode("utf-8")
            if "\n" in v or "\r" in v:
                v = v.replace("=","=3D").replace("\r","=0D").replace("\n","=0A")
                if ':' in mapTo: mapTo=mapTo[:mapTo.index(':')]+";ENCODING=QUOTED-PRINTABLE"+mapTo[mapTo.index(':'):]
                else: mapTo += ";ENCODING=QUOTED-PRINTABLE"
        o.write(mapTo+':'+v+'\r\n')
    for k,v in extra.items():
        if ';' in ''.join(v):
            sys.stderr.write("Warning: omitting "+k+" because don't know how to deal with the extra semicolons in it\n")
        else: o.write(k+':'+';'.join(v)+'\r\n')
    o.write("NOTE:Contact imported %d-%02d-%02d\r\n" % time.localtime()[:3]) # TODO: if there's already a NOTE, shouldn't we append this to the existing one instead of adding a new one?
    o.write("END:VCARD\r\n")
