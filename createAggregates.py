
# coding: utf-8

# In[2]:


from datetime import datetime
from matplotlib import pyplot as plt
from usageHelpers import *
import pandas as pd
import os, shutil
#get_ipython().run_line_magic('matplotlib', 'inline')


# In[28]:


source = "parsedFiles_prod\\"
target = "aggregates_prod\\"
if not os.path.exists(source):
    print (f"Source folder '{source}' is missing.  Run FileLoader to copy files from server'")
    exit()

if os.path.exists(target):
    shutil.rmtree(target)

os.makedirs(target)

logFile = "aggregator_" + "{:%Y_%m%d_%H%M}".format(datetime.now()) + ".log"

allFiles = os.listdir(source)
fileCnt = len(allFiles)


# In[4]:

cnt=0

frame = pd.DataFrame()
list_ = []

colNames = ["version", "studyKey", "sponsor", "pageType", "pageName", "yearMonth"]
for fStr in allFiles:
    cnt+=1
    if (cnt % 500 == 0):
        logger(logFile, f"Loading {cnt} of {fileCnt} for aggregation")
    df = pd.read_csv(source + fStr, header=None, index_col=None, names=colNames)
    list_.append(df)
frame = pd.concat(list_)

logger(logFile, f"All {fileCnt} files loaded")


# In[50]:

logger(logFile, f"Cleaning up all study keys that did not follow naming convention")


# clean-up - used data from a different study
frame["year"] = frame["yearMonth"].str[0:4].astype(int)
frame["pageName"] = frame["pageName"].str.replace("Custom_","")
frame["pageName"] = frame["pageName"].str.replace(r"[A-Za-z]+[\d]{3,}[\_]+","")
frame["pageName"] = frame["pageName"].str.replace(r"[0-9a-z]{8}\-[0-9a-z]{4}\-[0-9a-z]{4}\-[0-9a-z]{4}\-[0-9a-z]{12}","")
frame["pageName"] = frame["pageName"].str.replace("copy","")
logger(logFile, f"Creating aggregates for visits by page")


visitsByName = frame.groupby(["pageName", "year"]).size()
visitsByName2 = frame.groupby(["pageName", "yearMonth"]).size()
visitsByName.to_csv(path=target + "visitsByName.csv", header=True, index_label=["pageName", "year",  "visits"])
visitsByName2.to_csv(path=target + "visitsByName2.csv", header=True, index_label=["pageName", "yearMonth",  "visits"])


# In[31]:

logger(logFile, f"Creating aggregates for visits")

visits = frame.groupby("year").size()
visits2 = frame.groupby("yearMonth").size()
visits.to_csv(path=target + "visits.csv", header=True, index_label =["year", "visits"])
visits2.to_csv(path=target + "visits2.csv", header=True, index_label =["yearMonth", "visits"])


# In[60]:

logger(logFile, f"Creating aggregates for page name and type visits by study and sponsor")

pageByStudy = frame.groupby(["studyKey", "pageName"]).size()
pageByStudy.to_csv(path=target + "pageByStudy.csv", header=True, index_label =["studyKey", "pageName", "visits"])

pageBySponsor = frame.groupby(["sponsor", "pageName"]).size()
pageBySponsor.to_csv(path=target + "pageBySponsor.csv", header=True, index_label =["sponsor", "pageName", "visits"])

typeByStudy = frame.groupby(["studyKey", "pageType"]).size()
typeByStudy.to_csv(path=target + "typeByStudy.csv", header=True, index_label =["studyKey", "pageType", "visits"])

typeBySponsor = frame.groupby(["sponsor", "pageType"]).size()
typeBySponsor.to_csv(path=target + "typeBySponsor.csv", header=True, index_label =["sponsor", "pageType", "visits"])

types = frame.groupby("pageType").size()
types.to_csv(path=target + "types.csv", header=True, index_label =["pageType", "visits"])


# In[32]:


sponsors = frame["sponsor"].unique()
years = frame["year"].unique()
visitsBySponsor = frame.groupby(["sponsor", "year"]).size()
visitsBySponsor2 = frame.groupby(["sponsor", "yearMonth"]).size()
years.sort()
visitsBySponsor.to_csv(path=target + "visitsBySponsor.csv", header=True, index_label =["Sponsor", "year", "visits"])
visitsBySponsor2.to_csv(path=target + "visitsBySponsor2.csv", header=True, index_label =["Sponsor", "yearMonth", "visits"])


# In[25]:







visitsByStudy = frame.groupby(["studyKey", "year"]).size()
visitsByStudy2 = frame.groupby(["studyKey", "yearMonth"]).size()
visitsByStudy.to_csv(path=target + "visitsByStudy.csv", header=True, index_label =["studyKey", "year", "visits"])
visitsByStudy2.to_csv(path=target + "visitsByStudy2.csv", header=True, index_label =["studyKey", "yearMonth", "visits"])



visitsByType = frame.groupby([ "pageType", "year"]).size()
visitsByType2 = frame.groupby(["pageType", "yearMonth"]).size()
visitsByType.to_csv(path=target + "visitsByType.csv", header=True, index_label =["pageType", "year", "visits"])
visitsByType2.to_csv(path=target + "visitsByType2.csv", header=True, index_label =["pageType", "yearMonth", "visits"])

