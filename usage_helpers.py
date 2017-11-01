import os
from datetime import datetime
import pyodbc 

def getSponsor(tenantKey):
    # get the sponsor name given the tenantKey
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=TenantServer;"
                      "Database=TenantDatabase;"
                      "Trusted_Connection=yes;")

    cursor = cnxn.cursor()
    cursor.execute(f"SELECT Sponsor, TenantName FROM dbo.Tenants WHERE TenantKey='{tenantKey}'")
    row = cursor.fetchone()
    return row.Sponsor    

def logger(fileName, msg):
    # Helper method to log the debugg messages to file
    log = open(fileName, "a")
    dttime = str(datetime.now())[0:19]
    log.write("{} : {}\n".format(dttime, msg))
    log.close()


def parsePageName(pageLst, studyKey):
    # extract the page (skip Report and Metadata, those are redundant)
    if (len(pageLst) < 5):
        #return "/".join(pageLst[2:]) # home/index or something
        return ""

    flowOrReport = pageLst[-1]

    # Assume the first part is the studyKey or training
    flowParts = flowOrReport.split("_")
    try:
        flowParts.remove(studyKey)
    except ValueError:
        x = 1

    flowOrReport = "_".join(flowParts)

    # special case, ignore these ajax calls
    if (flowOrReport in {"PopulateCascadeDropdown", "LogOff"}):
        return ""

    # ignore pings
    if (pageLst[3] == "ping"):
        return ""


    pageName = f"{pageLst[3]}/{flowOrReport}"
    return pageName

