from usage_helpers import *
from pathlib import Path
from datetime import datetime
import os

# Given full set of web logs, extract the page visited.  Ignore the other lines in the log.

def writeLnToFile(filePath, msg):
    # This 
    isFile = Path(filePath)
    if isFile.is_file():
        fileObj = open(filePath,"a")
    else:
        fileObj = open(filePath,"w")
    fileObj.write(msg + "\n")
    fileObj.close()

source = "logFiles\\"
target = "parsedFiles\\"
if not os.path.exists(source):
    print (f"Source folder '{source}' is missing.  Run FileLoader to copy files from server'")
    exit()

if not os.path.exists(target):
    os.makedirs(target)

logFile = "parser_" + "{:%Y_%m%d_%H%M}".format(datetime.now()) + ".log"

# parse text to retrieve date, version, tenantKey, report (4 hours for 2000 files)

# This text is present, ignore the user cookie and just get the page name
requestText = "Creating RequestContext ... for "
ordinal = 1
cnt = 0
allFiles = os.listdir(source)
fileCnt = len(allFiles)
#results = {}
for fStr in allFiles:
    cnt+=1
    fileObj = open(source + fStr,"r").readlines() 
    lnParsed = 0
    lnCnt = len(fileObj)
    for line in fileObj:
        # TODO: put "metadata" and "reports" in an array to allow for easier additions 
        # TODO: since this is using MVC, maybe figure out a way to extract the controller and action away or include it in a report
        if requestText in line: # and ("Metadata/Flow/Show/" in line or "Reports/Report/View/" in line):
            lnParsed += 1
            entryMnth = line[0:7]
            # index = line.find(requestText) + len(requestText)
            # end = line.find(",", index)
            # login = line[index:end]

            index = line.find("Bracket")

            # skip any of the parameters and do not include new line
            end = line.find("?")
            if (end == -1):
                end = line.find("\n")

            page = line[index:end]
            page = page.split('/')

            if (len(page) < 3):
                continue 

            version = page[0][9:11]
            tenantKey = page[1]

            # extract the page name from string
            pageName = parsePageName(page, tenantKey)
            if (pageName == ""):
                continue

            # extract the page (skip Report and Metadata, those are redundant)
            # if (len(page) < 5):
            #     pageName = "/".join(page[2:]) 
            # else:
            #     pageName = "/".join(page[3:])

            # create a tuple of the information we need
            key = (version, tenantKey, pageName, entryMnth)

            # I thought about combining the data into a dictionary... might not be necessary            
            # if results.has_key(key):
            #     results[key] = results[key] + 1
            # else:
            #     results[key] = 1
            #outFile.write(",".join((entryDt, version, login, tenantKey, pageType, pageName)) + "\n")
            writeLnToFile(target + fStr, ",".join(key))
    logger(logFile, f"Finished with file {cnt} of {fileCnt}: extracted {lnParsed} lines of {lnCnt} from {fStr}")

logger(logFile, "Finished with all files")


# resFile = open("output\\results.{}.csv".format(str(datetime.now())[0:19]), "w")
# for k, p in results.items():
#     resFile.write(",".join((str(k[0]), str(k[1]), str(k[2]), str(k[3]), str(p))) + "\n")

# resFile.close()
    

