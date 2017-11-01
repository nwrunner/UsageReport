
# coding: utf-8

# In[20]:


from datetime import datetime
from matplotlib import pyplot as plt
from usageHelpers import *
import pandas as pd
import os
import shutil


# In[21]:


source = "aggregates_prod\\"
target = "images_prod\\"
if not os.path.exists(source):
    print (f"Source folder '{source}' is missing.  Run FileLoader to copy files from server'")
    exit()

# delete old results and re-create
if not os.path.exists(target):
    os.makedirs(target)

logFile = "images_" + "{:%Y_%m%d_%H%M}".format(datetime.now()) + ".log"


frame = pd.read_csv(source + "pageBySponsor.csv", header=0)
del frame['0'] # remove random 4th column
width = 0.5 # the width of the bars 
sponsors = frame["sponsor"].unique()
bracketBlue = "#0092d0"
report = "PageVisits\\"
if os.path.exists(target+report):
    shutil.rmtree(target+report)
os.makedirs(target + report)

for sponsor in sponsors:
    title = f'Page Visits for {sponsor}'
    frameSponsor = frame.query(f"sponsor=='{sponsor}'")
    frameSponsor.reset_index(drop=True, inplace=True) # re-index to start df at 0

    x = frameSponsor["pageName"]
    y = frameSponsor["visits"]
    ind = y.index # 0 to N-1

    fig, ax = plt.subplots(1,1, figsize=(20,ind.size/2))
    ax.set_xscale("linear")
    ax.barh(ind, y, width, color=bracketBlue)
    ax.set_yticks(ind)
    ax.set_yticklabels(x, minor=False)
    plt.title(title, fontsize=20, fontweight="bold")
    plt.xlabel('Visit Count', fontsize=20, fontweight="bold")
    plt.ylabel('Page Name', fontsize=20, fontweight="bold")  
    for i, v in enumerate(y):
        ax.text(v + 0.5, i, str(v), color='blue')
    plt.ylim([0,ind.size])
    logger(logFile, f"Creating Page visits per sponsor for '{sponsor}'")
    plt.savefig(target+report+f"PageVisits_{sponsor}",bbox_inches='tight', pad_inches=0.1)
    plt.close()




frame = pd.read_csv(source + "pageByStudy.csv", header=0)
del frame['0'] # remove random 4th column
width = 0.5 # the width of the bars 
studies = frame["studyKey"].unique()
bracketBlue = "#0092d0"
report = "PageVisitsStudy\\"
if os.path.exists(target+report):
    shutil.rmtree(target+report)
os.makedirs(target + report)

for study in studies:
    title = f'Page Visits for {study}'
    tmpFrame = frame.query(f"studyKey=='{study}'")
    tmpFrame.reset_index(drop=True, inplace=True) # re-index to start df at 0

    x = tmpFrame["pageName"]
    y = tmpFrame["visits"]
    ind = y.index # 0 to N-1

    fig, ax = plt.subplots(1,1, figsize=(20,ind.size/2))
    ax.set_xscale("linear")
    ax.barh(ind, y, width, color=bracketBlue)
    ax.set_yticks(ind)
    ax.set_yticklabels(x, minor=False)
    plt.title(title, fontsize=20, fontweight="bold")
    plt.xlabel('Visit Count', fontsize=20, fontweight="bold")
    plt.ylabel('Page Name', fontsize=20, fontweight="bold")  
    for i, v in enumerate(y):
        ax.text(v + 0.5, i, str(v), color='blue')
    plt.ylim([0,ind.size])    
    logger(logFile, f"Creating Page visits per study for '{study}''")
    plt.savefig(target+report+f"PageVisits_{study}",bbox_inches='tight', pad_inches=0.1)
    plt.close()

    


# In[ ]:





# In[ ]:


# sponsors = frame["sponsor"].unique()
# years = frame["year"].unique()
# visitsBySponsor = frame.groupby(["year", "sponsor"]).size()
# visitsBySponsor2 = frame.groupby(["yearMonth", "sponsor"]).size()
# years.sort()
# visitsBySponsor.to_csv(path=target + "visitsBySponsor.csv", header=True, index_label =["year", "Sponsor", "visits"])
# visitsBySponsor2.to_csv(path=target + "visitsBySponsor2.csv", header=True, index_label =["yearMonth", "Sponsor", "visits"])


# In[ ]:





# In[ ]:


# for sp in sponsorPlots.keys():
#     dataList = sorted(sponsorPlots[sp].items())
#     x,y = zip(*dataList)
#     plt.plot(x,y)
# plt.legend(sponsorPlots.keys())


# In[ ]:


# sponsorPlots = {} # dictionary of dictionary year + cnt
# for k, v in visitsBySponsor.items():
#     sponsor = k[1]
#     year = k[0]
#     if (sponsor in sponsorPlots):
#         dict = sponsorPlots[sponsor]
#         dict[year] = v
#     else:
#         sponsorPlots[sponsor] = {year: v}

