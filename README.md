# UsageReport
Parse through log files and create aggregate images of the results.  

usage_helpers.py
 - Helper methods 

FileLoader.py 
 - First file.  This copies all log files locally.  Recommend that this is run through command line rather than in an IDE
 - Update "sources" array to include the folder(s) of the log files

ParseFile.py
 - After copying files locally, parse to look for page hits.  Extract the data we want to keep in a new file

createAggregates.py
 - Create aggregate files in CSV using pandas dataframes.  Could do a little better job slicing the data in more meaning file manner if there was more time to play around

createImages.oy
 - Create some images with the resulting CSV files.  
