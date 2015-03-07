#!/usr/bin/python

import csv
import sys
from optparse import OptionParser

class Panel:
	name = ""
	description = ""
	adult = ""
	day = ""
	startTime = ""
	room = ""
	guideNames = []
	
def printPanels(filename):
        # Open the output file
        outputFile = open(outputFilename, 'w')

        # Set up the HTML file
        outputFile.write("<html>\n")
        outputFile.write("<head>\n")
        outputFile.write("<title>Panel Schedule</title>\n")
        outputFile.write("</head>\n")
        outputFile.write("<body>\n")

        # Write out the panels
	for panel in grouped_panels:
		outputFile.write("<hr />\n")
		outputFile.write("<p><strong>Panel Title:</strong><br />\n")
		outputFile.write("<em>" + panel.name + "</em></p>\n")
		outputFile.write("<p><strong>Panel Description:</strong></p>\n")
		outputFile.write("<p>" + panel.description + "</p>\n")
		outputFile.write("<p><strong>Panelist Guide Names:</strong>\n")
                outputFile.write("<ul>\n")
		for panelist in panel.guideNames:
			outputFile.write("<li>" + panelist + "</li>\n")
                outputFile.write("</ul></p>\n")
		outputFile.write("<p><strong>Adult Panel:</strong> " + panel.adult + "</p>\n")
		outputFile.write("<p><strong>Day:</strong> " + panel.day + "</p>\n")
		outputFile.write("<p><strong>Room:</strong> " + panel.room + "</p>\n")
		outputFile.write("<p><strong>Start Time: </strong>" + panel.startTime + "</p>\n")

        # Close out the HTML and the output file
        outputFile.write("</body>\n")
        outputFile.write("</html>\n")
        outputFile.close()

# Parse command line options
usage = "usage: %prog panel_list output_html_file"
parser = OptionParser(usage=usage)

(options, args) = parser.parse_args()
if len(args) < 2:
	parser.error("incorrect number of args")
	
panelListFilename = args[0]
outputFilename = args[1]

# Load up the list file
panelListFile = open(panelListFilename, 'r')
panelListReader = csv.DictReader(panelListFile)



# Allocate an empty dictionary to hold our panels grouped by the (title, description)
# (title, description, adult, day, startTime, room) tuple
groupedPanels = []

for row in panelListReader:
	# This is where things get interesting.
	# We want to use the panel name and the panel description as a tuple key in a
	# dictionary so that even though they may appear multiple times within the query,
	# they will be grouped together when printing out. This may not be the most
	# efficient way to do this, but it's the easiest.
	# Anyway, the easiest way to add to a dictionary is to just try to access the
	# key you want to add to. However, since we're going to want to append to a list
	# there, we can't do that.
	# Therefore, we will try to *read* from the key we try to add to. If there is
	# nothing there, it will throw a KeyError exception, which we'll catch and *then*
	# allocate a new list to be inserted at that key. If the exception is not thrown,
	# then we can just append to the existing list.
	#print row
	newPanel = Panel()
	newPanel.name = row['Panel Name']
	newPanel.description = row['Program Guide Description']
	newPanel.adult = row['Adult Panel']
	newPanel.day = row['Day']
	newPanel.startTime = row['Start Time']
	newPanel.room = row['Panel Room']
	newPanel.guideNames = []
	
	if len(groupedPanels) == 0:
		groupedPanels.append(newPanel)
	else:
		if groupedPanels[len(groupedPanels) - 1].name == newPanel.name:
			newPanel = groupedPanels[len(groupedPanels) - 1]
		else:
			groupedPanels.append(newPanel)
			
	newPanel.guideNames.append(row['Guide Name'])
	
	#print newPanel.name
	#for panelist in newPanel.guideNames:
	#	print panelist
	#print "\n"

# Now we can go through our grouped panels and print everything out, nicely formatted.
# Yeah, no word wrap, but who cares.

printPanels()

# Close and clean up
panelListFile.close()
