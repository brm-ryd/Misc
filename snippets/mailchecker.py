#!/usr/bin/python
"""
Simple method to verify email address through MX servers
need to improve the exception of error message socket
"""

import smtplib, os, sys, socket

if len(sys.argv) < 2:
	print "use: " + sys.argv[0] +" + email_address"
	exit(1)
email = sys.argv[1]
maildomain = email.split("@")[-1]
nstoken = "mail exchanger = "
mailserver = ""
m = []
print "check mx server ..."
plines = os.popen("nslookup -type=mx " + maildomain).readlines()
for pline in plines:
	if nstoken in pline:
		mailserver = pline.split(nstoken)[1].strip()
		mailserver = mailserver.split(" ")[-1] #no need this line in windows env
		m.append(mailserver)
		

if mailserver == "":
	print "unable to get mx server ...", maildomain
	exit(1)
else:
	print "found mx mail... ", m
print "checking email address ....", email
for i in m:
	socket.setdefaulttimeout(4)
	try:
		s = smtplib.SMTP(i)
	except (socket.timeout, smtplib.SMTPException), e:
		print "this mx server time out ", i, e
		pass
	else:
		rep1 = s.ehlo()
		if rep1[0] == 250:
			rep2 = s.mail("test@rediff.com")
			if rep2[0] == 250:
				rep3 = s.rcpt(email)
			if rep3[0] == 250:
				print email, " valid - mxserver: ", i 
			elif rep3[0] == 550:
				print email, " invalid"
