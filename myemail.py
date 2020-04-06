#!/usr/bin/python3

"""
myemail.py

Copyright (C) 2016  hjltu@ya.ru

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

usage: python3 myemail.py [name, IP, token]
"""

import smtplib
import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from config.hjsite import SMTP_SERVER, SMTP_PORT, FROM_EMAIL, FROM_EMAIL_PASSWD, TO_EMAILS
from setup.serial import serial as SERIAL
from email.mime.text import MIMEText

MSG_SUBJECT = "New account confirmation"

def main(args):
    if not isinstance(TO_EMAILS, list):
        return "No recipient"
    to = args[0]
    link = args[1]
    token = args[2]
    text = """<pre>
    Welcome! {} from {}
    This message from http://{}
    Thanks for signing up. If you are already logged in
    Please follow this link to confirm registration:
        <a style="font-weight:bold"
        href="http://{}:5000/confirm/{}">Confirm</a>
    Cheers!</pre>
    """.format(to, SERIAL, link, link, token)

    msg = MIMEText(text ,'html')
    msg['Subject'] = MSG_SUBJECT
    msg['From'] = FROM_EMAIL
    msg['To'] = to

    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    server.ehlo()
    server.login(FROM_EMAIL, FROM_EMAIL_PASSWD)
    print("send to:", to)
    for email in TO_EMAILS:
        try:
            server.sendmail(email , msg.as_string())
        except Exception as e:
            print(e)
    server.quit()

if(__name__=='__main__'):
    main(sys.argv[1:])

