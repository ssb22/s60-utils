# s60-utils
Python utilities for old Nokia/Symbian S60 phones, from http://ssb22.user.srcf.net/s60/
(also mirrored at http://ssb22.gitlab.io/s60/ just in case)

You will need Python on the phone: install [PyS60](https://garage.maemo.org/frs/download.php/5952/Python_1.9.4.sis) and [ScriptShell](https://garage.maemo.org/frs/download.php/5910/PythonScriptShell_1.9.4_3rdEd.sis) (those links are for 3rd edition phones; for other editions google it).  You can put Python on one of the default softkeys to launch it faster (on my device the control for this is located in Menu / Settings / Phone / General / Personalization / Standby mode / Shortcuts).

* [A simple stopwatch for S60](stopwatch.py) (because at least some models don't have one as standard)
* [Auto-answer](auto-answer.py) if you want to let someone call you to listen to a meeting without your having to worry about answering the phone. Can optionally be set to text them at the meeting's start time if they haven't called yet.
* [Backup SMS inbox to text file](backup-inbox.py) a simple script that backs up the phone's SMS inbox to a text file on the memory card (useful if you can't use PC Suite but want to read/save the SMS on a computer)
* [Backup contacts to text file](backup-contacts.py) a simple script that backs up your phone's contact list to a text file full of VCARD entries on the memory card (useful if you can't use the PC Suite to back up). To restore, here is a [script to import all contacts from the VCARD (VCF) file](restore-contacts.py) (S60 can usually open the VCARD file itself without this, but some versions show just the first card).
* [Backup contacts to CSC file](contacts2csc.py) like the above but writes the .CSC format used by the Windows Mobile application `PIM Backup`. This can be used to copy your S60 contacts to Windows Mobile without needing a Windows PC. After PIM Backup has been run once, it sets itself to be able to open these CSC files; should work on any WM2005+ device with or without touchscreen (but not Windows Phone 7 or above which is a different system).
    * In my separate repository `wm6-utils`, there is a script to convert CSC back to VCF (`csc2vcf.py`) for copying Windows Mobile contacts to S60, Android etc, plus a script to format message dumps from Windows Mobile (`csm2txt.py`) and recover text from the Windows Mobile Notes app (`pwi2txt.sh`).
    * PIM Backup's `.pib` files are actually zip files that can contain these CSCs as well as message files etc.  You can manipulate them with Unix tools---for example, to generate a report of a WM phone's SMS delivery failures, first back up the contacts and messages, then unzip the .pib file and do something like `set -o pipefail;for Num in $(iconv -f UTF-16 -t UTF-8 &lt; msgs_*.csm | grep "message you sent to .* was not delivered" |sed -e "s/.*message you sent to //" -e "s/was not delivered.*//" -e 's/+44/0/'|sort|uniq); do echo -n "$Num: "; iconv -f UTF-16 -t UTF-8 &lt; contacts_*.csc | grep $(echo $Num|sed -e s/0//)|sed -e 's/";.*//' -e 's/"//' || echo '(unknown)';done`
* [To-Call List](tocall.py): takes a text file of notes (one per line) and formats it for your phone's Web browser, adding links to any phone numbers and to any of your phone's contacts whose names are mentioned. You can then browse through the notes and directly call the numbers. (If in the EU you must comply with the 2018 GDPR and not keep written notes about any person who has not given you permission to do so. Although the GDPR supposedly grants exemption to "personal or household activities", preliminary ruling C-25/17 point 21 implies that an individual doing something as innocuous as recommending their club, if it causes people to *think* this amounts to working for the club, could be breaking the law by using a notes file.)
* [Cleanup](cleanup.py): Deletes browser cache files, downloads, interrupted downloads etc that are kept in C: folders not usually shown.

Legal
=====
These scripts were placed into the public domain by Silas S. Brown.
Android is a trademark of Google LLC.
Python is a trademark of the Python Software Foundation.
Unix is a trademark of The Open Group.
Windows is a registered trademark of Microsoft Corp.
Any other trademarks I mentioned without realising are trademarks of their respective holders.
