#!/usr/bin/python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import smtplib
import csv
import sys
import datetime
from optparse import OptionParser
from email.message import Message

class Panel:
    def __init__(self, name, day, time, length, room, organizer):
        self.name = name
        self.day = day
        self.time = time
        self.length = length
        self.room = room
        self.organizer = organizer

class Panelist:
    def __init__(self, email, firstName, lastName):
        self.email = email
        self.firstName = firstName
        self.lastName = lastName

# Global constants
DEFAULT_SERVER = "smtp.comcast.net"
FROM_ADDRESS = "panels@animeboston.com"
FROM_TITLE = "Anime Boston Panels Coordinator"
SUBJECT = "Your Anime Boston Panel Itinerary"

# Parse command line options
usage = "usage: %prog [-s server] [-p port] [-f from_address] panel_list template"
parser = OptionParser(usage=usage)
parser.add_option("-s", action="store", type="string", dest="serverName",
                  default=DEFAULT_SERVER, help="SMTP server name")
parser.add_option("-p", action="store", type="int", dest="port",
                  help="SMTP server port")
parser.add_option("-f", action="store", type="string", dest="from_address",
                  default=FROM_ADDRESS, help="From address")
parser.add_option("-t", action="store", type="string", dest="subject",
                  default=SUBJECT, help="Subject")

(options, args) = parser.parse_args()
if len(args) < 2:
    parser.error("incorrect number of args")
   
panelListFn = args[0]
templateFile = args[1]

# Set the year
year = str(datetime.date.today().year)

# Load up the template file
templateFo = open(templateFile, 'r')
template = templateFo.read() # Read in the whole thing.
templateFo.close()

# Set up empty dictionary of panelists
panelists = {}

# Load up the list file
panelListFile = open(panelListFn, 'r')
panelListReader = csv.DictReader(panelListFile)

# Just digging through the reader for now to see what we got.
for row in panelListReader:
    organizer = Panelist(row["EmailAddress"], row["FirstName"], row["LastName"])
    currentPanel = Panel(row["PanelName"], row["Day"], row["StartTime"], row["PanelLength"],
                         row["PanelRoom"], organizer)
    if row["EmailAddress"] in panelists:
        # If it already is in the dictionary, append it to the list
        panelists[row["EmailAddress"]].append(currentPanel)
    else:
        # Add a new list to the dictionary
        panelists[row["EmailAddress"]] = [currentPanel]
        
for current in panelists.keys():
    bodyText = template
    # Insert first and last name
    bodyText = bodyText.replace("<FirstName>", panelists[current][0].organizer.firstName)
    bodyText = bodyText.replace("<LastName>", panelists[current][0].organizer.lastName)
    
    # Now loop through and generate the panel list
    allPanels = ""
    for thePanel in panelists[current]:
        allPanels = allPanels + "Panel Name: " + thePanel.name + "\n"
        allPanels = allPanels + "Day: " + thePanel.day + "\n"
        allPanels = allPanels + "Time: " + thePanel.time + "\n"
        allPanels = allPanels + "Length in minutes: " + thePanel.length + "\n"
        allPanels = allPanels + "Room: " + thePanel.room + "\n\n"
            
    bodyText = bodyText.replace("<ScheduledPanels>", allPanels)
    
    # Now we can email this out.
    emailBody = "To: " + current + "\n"
    emailBody = emailBody + "From: " + FROM_TITLE + " <" + options.from_address + ">\n"
    emailBody = emailBody + "Subject: " + options.subject + "\n\n"
    emailBody = emailBody + bodyText
    # Connect to the server and send the mail
    if (options.port == None):
        server = smtplib.SMTP(options.serverName)
    else:
        server = smtplib.SMTP(options.serverName, options.port)
    print "Sending mail to: " + current
    server.sendmail(FROM_ADDRESS, current, emailBody)
    server.quit()

# Close and clean up
panelListFile.close()

