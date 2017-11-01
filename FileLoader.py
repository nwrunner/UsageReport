# First file, update the sources to the path of log files if there's a change

import os
import re
from datetime import datetime
import shutil
import usage_helpers

# Get sources (backup from production)
sources = []
sources.append("\\\\Backup\\dDrive\\log\\2013\\")
sources.append("\\\\Backup\\dDrive\\log\\2014\\")
sources.append("\\\\Backup\\dDrive\\log\\2015\\")
sources.append("\\\\Backup\\dDrive\\log\\2016\\")

# local path for output
target = "logFiles\\"

if not os.path.exists(target):
    os.makedirs(target)

# only copy Web and mobile logs
# Skip Entity Framework SQL logs, rendering engine logs, and 3rd party Ibatis report logs
logPattern = "[A-Z\d]+\_Web\d{2}\.log"
logFile = "getLogs_" + "{:%Y_%m%d_%H%M}".format(datetime.now()) + ".txt"

# count the total number of files copied and scanned
totalCnt = 0

# Get all files that match the name and copy (~300kb/s so this will take some time ~15gb of files to scan)
# Recommend running in cmd shell and not VS Code so you can do other things while copy is running in the background
for source in sources:
    allFiles = os.listdir(source)
    sourceCnt = len(allFiles)
    cnt = 0
    logger(logFile, f"Scanning {sourceCnt} files from {source}'")
    for fileName in allFiles:
        if (re.search(logPattern, fileName)):
            cnt += 1
            logger(logFile, f"Copying '{fileName}'")
            shutil.copy2(source+fileName, target+fileName)
            #fileList.append(fileName)
    totalCnt += cnt
    logger(logFile, f"Copied {cnt} out of {sourceCnt} from {source}")

logger(logFile, f"Total number of files = {totalCnt}")

