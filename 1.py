#!/usr/bin/env python
#coding=utf8
from cStringIO import StringIO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email import Charset
import email.encoders
import quopri
from email.generator import Generator
from email.utils import formataddr 
import smtplib
import codecs
import getpass

# Tip: To generate a plain-text version of the HTML file:
# $ lynx -display_charset=utf-8 -width=1024 -dump htmlnewsletter.html > htmlnewsletter.txt

########## ENTER SETTINGS HERE ##############

# Data for header
from_address_email = 'danielcameron777test@gmail.com'
from_address_name = u'Dennis'
subject = u'Test'

# Email server and port
# server = 'your.email.server'
server = 'smtp.gmail.com'
port = 587

# Data for file locations
# Everything should be in this directory (relative to where this python script lives).
# If the directory is the same as the other files, then this should be './'
# The directory should end with a slash ('/')
directory = './'
# Location of list of recipient addresses in a plain text file in this format:
# "Display name" <email@address>
# "Another display name" <email@address>
# etc. (Don't include the '#' signs)
to_addresses_file = directory + 'address_list.txt'
print("Thanks", to_addresses_file)
# The HTML version of the message body
htmlcontent = directory + 'htmlVersionOfMessage.html'
# The text-only version of the message body
textcontent = directory + 'plainTextVersionOfMessage.txt'

########## NO USER-ENTERABLE DATA BELOW THIS LINE ###########

# Parse out the username from the email address
username = from_address_email.split('@')[0]
print("ddd", username)
 
# Format from address to be included in the header.
from_address = [from_address_name, from_address_email.upper()]
print("from_address", from_address[1])

# Default encoding mode set to Quoted Printable. Acts globally!
Charset.add_charset('utf-8', Charset.QP, Charset.QP, 'utf-8')
 
# 'alternative' MIME type --- HTML and plain text bundled in one e-mail message
msg = MIMEMultipart('alternative')

# Create subject line. This is converted to non-Unicode because of the use of str().
msg['Subject'] = str(Header(subject, 'utf-8'))

# Create and format From line
msg['From'] = '"{0}" <{1}>'.format(Header(from_address[0], 'utf-8'), from_address[1])
print("from", msg['From'])
 
# Read To: addresses from a file in this format:
# "Display name" <email@address>
# "Another display name" <email@address>
# etc.
if __name__ == "__main__":
    import sys
    with codecs.open(directory + to_addresses_file, 'r', 'utf-8') as f:
       addresses = f.read().splitlines()
else: # This could be an alternative script for interactive testing
    import sys
    with codecs.open(directory + to_addresses_file, 'r', 'utf-8') as f:
     addresses = f.read().splitlines()
print("address:", addresses)
# Parse the To: address input
# Only descriptive part of recipient and sender shall be encoded, not the email address
recipients = ''
recipientAddrList = [] 
for i, addresspair in enumerate(addresses):
 name = addresses[i].split('"')[1]
 address = addresses[i].split('<')[1].split('>')[0]
 # If no recipients have been added yet (i.e. if this is the first recipient)
 if len(recipients) == 0:
  # The output of the format() and str() commands are not Unicode.
  recipients = recipients + '"{0}" <{1}>'.format(Header(name, 'utf-8'), address)
  recipientAddrList.append(str(address))
 else:
  recipients = recipients + ', "{0}" <{1}>'.format(Header(name, 'utf-8'), address)
  recipientAddrList.append(str(address))

# Create To line
msg['To'] = recipients

# Read in data for the message body from files
text = codecs.open(textcontent, 'r', 'utf-8').read()
html = codecs.open(htmlcontent, 'r', 'utf-8').read()

# Use this if you don't want to use UTF-8
# html = open(htmlcontent, 'r').read()
 
# Encode and attach both parts to the message. The text part should come first.
textpart = MIMEText(text.encode('utf-8'), 'plain', 'UTF-8')
textpart.replace_header('content-transfer-encoding', 'quoted-printable')
# textpart.set_payload(u'happy face ☺', 'utf-8')
htmlpart = MIMEText(html.encode('utf-8'), 'html', 'UTF-8')
htmlpart.replace_header('content-transfer-encoding', 'quoted-printable')
# htmlpart.set_payload(u'happy face ☺', 'utf-8')
msg.attach(textpart)
msg.attach(htmlpart)
# ps = email.encoders.encode_quopri("hello world")
# email.encoders.encode_quopri(msg.as_string)

# Get the password from the user
pw = getpass.getpass('Enter e-mail account password for ' + username + ':')
print("password", pw) 
# Send the message
s = smtplib.SMTP(server, port)
# s = smtplib.SMTP('mail.google.com')
s.set_debuglevel(0)
s.ehlo()
s.starttls()
s.ehlo()
s.login(from_address_email, pw)
s.sendmail(str(from_address[1]), recipientAddrList, msg.as_string())