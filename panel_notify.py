#!/usr/bin/python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import smtplib
import csv
import sys
from optparse import OptionParser

# Global constants
DEFAULT_SERVER = "smtp.comcast.net"
FROM_ADDRESS = "panels@animeboston.com"
FROM_TITLE = "Anime Boston Panels Coordinator"
SUBJECT = "Your Anime Boston Panel Application"

# Parse command line options
usage = "usage: %prog [options] panel_list template\n"\
	"\t-s server_name\n"\
	"\t-p port\n"\
	"\t-t subject\n"\
	"\t-f from_address"

parser = OptionParser(usage=usage)
parser.add_option("-s", action="store", type="string", dest="server_name",
				  default=DEFAULT_SERVER,
				  help="SMTP server name")
parser.add_option("-p", action="store", type="int", dest="port",
				  help="SMTP server port")
parser.add_option("-t", action="store", type="string", dest="subject",
				  default=SUBJECT, help="Email subject")
parser.add_option("-f", action="store", type="string", dest="from_address",
		  default = FROM_ADDRESS, help="From address")

(options, args) = parser.parse_args()
if len(args) < 2:
	parser.error("incorrect number of args")
	
panel_list_fn = args[0]
template_file = args[1]

# Load up the  template file
template_fo = open(template_file, 'r')
template = template_fo.read() # Read in the whole thing.
template_fo.close()

# Load up the list file
panel_list_file = open(panel_list_fn, 'r')
panel_list_reader = csv.DictReader(panel_list_file)

# Iterate through the csv DictReader and send out emails.

for row in panel_list_reader:
	body_text = template
	for heading in row.keys():
		search_string = "<" + heading + ">"
		# If the template/body_text has more than one option, we need to loop thorugh it
		# several times.
		# Probably not the most efficient technique, but I'm lazy and it works.
		body_text = body_text.replace(search_string, row[heading])
			
	email_body = "To: " + row["EmailAddress"] + "\n"
	email_body = email_body + "From: " + FROM_TITLE + " <" + options.from_address \
	             + ">" + "\n"
	email_body = email_body + "Subject: " + options.subject + "\n\n" + body_text
	
	# Connect to the server and send the mail
	if (options.port == None):
		server = smtplib.SMTP(options.server_name)
	else:
		server = smtplib.SMTP(options.server_name, options.port)
	print "Sending mail to: " + row["EmailAddress"]
	server.sendmail(FROM_ADDRESS, row["EmailAddress"], email_body)
	# Send a copy to myself to be safe so I can review it in case there are any bugs.
        # server.sendmail(FROM_ADDRESS, "dragonmaster.lou@gmail.com", email_body)
	server.quit()

# Close and clean up
panel_list_file.close()
