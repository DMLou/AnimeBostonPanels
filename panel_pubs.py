#!/usr/bin/python

import csv
import sys
from optparse import OptionParser

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

# Open the output file
outputFile = open(outputFilename, 'w')

# Allocate an empty dictionary to hold our panels grouped by the (title, description)
# tuple
groupedPanels = {}

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
	try:
		panelistList = \
			groupedPanels[(row['PanelName'], row['ProgramGuideDescription'])]
	except KeyError:
		# If we get this exception, it means that we didn't create this entry
		# in the dictionary yet. Let's create a list to store what we got.
		groupedPanels[(row['PanelName'], row['ProgramGuideDescription'])] = \
			[row['GuideName']]
	else:
		panelistList.append(row['GuideName'])

# Now we can go through our grouped panels and print everything out, nicely formatted
# in HTML!
outputFile.write("<html>\n")
outputFile.write("<head>\n")
outputFile.write("<title>Panels for Publications</title>\n")
outputFile.write("</head>\n")
outputFile.write("<body>\n")

for key in groupedPanels.keys():
	outputFile.write("<hr />\n")
	title, description = key
	outputFile.write("<p><strong>Panel Title:</strong><br />" + title + "</p>\n")
	outputFile.write("<p><strong>Panel Description:</strong><br />\n")
	outputFile.write(description + "</p>\n")
	outputFile.write("<p><strong>Panelist Guide Names:</strong>\n")
        outputFile.write("<ul>\n")
	for panelist in groupedPanels[key]:
		outputFile.write("<li>" + panelist + "</li>\n")
        outputFile.write("</ul></p>\n")

outputFile.write("</body>\n")
outputFile.write("</html>\n")

# Close and clean up
panelListFile.close()
outputFile.close()

