#!/usr/bin/python

import csv
import sys

# Global constants
# For the source file, unmodified from the CSV dump
ASSOCIATE_DELIMITER = '|'
ASSOC_COLUMN_SRC = "assoc_total"
AGREED_COLUMN_SRC = "assoc_agree"
REGISTERED_COLUMN_SRC = "assoc_reg"
FIRSTNAME_COLUMN_SRC = "assoc_first_name"
LASTNAME_COLUMN_SRC = "assoc_last_name"
PROGRAMGUIDENAME_COLUMN_SRC = "assoc_pg_name"
EMAIL_COLUMN_SRC = "assoc_email"
PHONE_COLUMN_SRC = "assoc_phone1"
PHONETYPE_COLUMN_SRC = "assoc_phone1_type"

# For the target file, based on what's in the target database
REGISTERED_COLUMN_TGT = "PreRegistered"
FIRSTNAME_COLUMN_TGT = "FirstName"
LASTNAME_COLUMN_TGT = "LastName"
PROGRAMGUIDENAME_COLUMN_TGT = "GuideName"
EMAIL_COLUMN_TGT = "EmailAddress"
MOBILE_PHONE_COLUMN_TGT = "MobileNumber"
HOME_PHONE_COLUMN_TGT = "PhoneNumber"
PANELIST_TYPE_COLUMN_TGT = "PanelistType"

# Parse command line options
usage = "usage: " + sys.argv[0] + " input_file output_file"
if len(sys.argv) < 2:
    print usage

inputFilename = sys.argv[1]
outputFilename = sys.argv[2]

# Load up the input file
inputFile = open(inputFilename, 'r')
inputFileReader = csv.DictReader(inputFile, delimiter=',')

# Create the output file
outputFieldNames = [REGISTERED_COLUMN_TGT, FIRSTNAME_COLUMN_TGT, LASTNAME_COLUMN_TGT,
                    PROGRAMGUIDENAME_COLUMN_TGT, EMAIL_COLUMN_TGT, MOBILE_PHONE_COLUMN_TGT,
                    HOME_PHONE_COLUMN_TGT, PANELIST_TYPE_COLUMN_TGT]
outputFile = open(outputFilename, 'w')
outputFileWriter = csv.DictWriter(outputFile, outputFieldNames)
outputFileWriter.writeheader()

# Iterate through the csv DictReader and process the associate panelists names

for row in inputFileReader:
    outputRow = {}
    numAssociates = row[ASSOC_COLUMN_SRC]
    agreed = row[AGREED_COLUMN_SRC]
    registered = row[REGISTERED_COLUMN_SRC]
    firstNames = row[FIRSTNAME_COLUMN_SRC].split(ASSOCIATE_DELIMITER)
    lastNames = row[LASTNAME_COLUMN_SRC].split(ASSOCIATE_DELIMITER)
    programGuideNames = row[PROGRAMGUIDENAME_COLUMN_SRC].split(ASSOCIATE_DELIMITER)
    emailAddresses = row[EMAIL_COLUMN_SRC].split(ASSOCIATE_DELIMITER)
    phoneNumbers = row[PHONE_COLUMN_SRC].split(ASSOCIATE_DELIMITER)
    phoneTypes = row[PHONETYPE_COLUMN_SRC].split(ASSOCIATE_DELIMITER)

    for i in range(int(numAssociates)):
        outputRow[REGISTERED_COLUMN_TGT] = registered
        outputRow[FIRSTNAME_COLUMN_TGT] = firstNames[i]
        outputRow[LASTNAME_COLUMN_TGT] = lastNames[i]
        outputRow[PROGRAMGUIDENAME_COLUMN_TGT] = programGuideNames[i]

        if len(emailAddresses[i]) == 0:
            outputRow[EMAIL_COLUMN_TGT] = "UNKNOWN"
        else:
            outputRow[EMAIL_COLUMN_TGT] = emailAddresses[i]
            
        if phoneTypes[i] == "Mobile":
            outputRow[MOBILE_PHONE_COLUMN_TGT] = phoneNumbers[i]
        else:
            outputRow[HOME_PHONE_COLUMN_TGT] = phoneNumbers[i]

        outputRow[PANELIST_TYPE_COLUMN_TGT] = "FAN" # Manually change when reviewing

        outputFileWriter.writerow(outputRow)
          
# Close and clean up
inputFile.close()
outputFile.close()
