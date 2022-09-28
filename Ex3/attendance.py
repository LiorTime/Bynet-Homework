#!/usr/bin/env python
# coding: utf-8


# --------------------------------------
import pandas as pd
import glob
import sys
import os
import os.path
from os import walk
from os.path import isfile, join
import hashlib
# --------------------------------------

if (len(sys.argv) < 2):
	print("No argument was given or too few.\nUse: attendance.py [directory=]")
	sys.exit(1)

directory = sys.argv[1] #Takes all files in path and runs on them
f = []
fp = []

cwd = os.getcwd() #gets current directory
cdcwd = cwd+"/"+directory #go to user input directrory
search = directory+"/participant-*"
hash_md5 = hashlib.md5()

def getListDirFiles(searchFile):
	for item in glob.glob(searchFile):
		f.append(os.path.basename(item))
		fp.append(item)	
	return f, fp
	
def createDir(dirname):
	dirct = os.path.join(cdcwd, dirname)
	if not os.path.exists(dirct):
		os.mkdir(dirct)
	return dirct, dirname

unique_files = dict()
def remDups(fileList):
	for item in fileList:
		h_file = hashlib.md5(open(item, 'rb').read()).hexdigest()
		if h_file not in unique_files:
			unique_files[h_file] = item
		else:
			os.remove(item)
			
filesList, filepList = getListDirFiles(search)
remDups(filepList) #removes duplicates
pth, newdir = createDir("Attendance") #pth is path to csv_files/Attendance

def getKey():
    df_key = pd.DataFrame()
    df_sample = pd.read_csv(cdcwd+"/"+filesList[0], encoding="UTF-16LE", sep="\t")
    df_sample = df_sample.drop_duplicates(subset=['Attendee Email'])
    
    df_sample = df_sample.set_index('Attendee Email')
    df_key['Attendee Email'] = df_sample.index
    df_key = df_key.set_index('Attendee Email')
    
    df_key['Name'] = df_sample['Name']
    
    return df_key

df_key = getKey() #starts a new table which will also stores our key email values from the sample
df_key = df_key.sort_values(by=['Name'])

def pullRelData(df):
	df[['Attendance Time','M']] = df['Attendance Duration'].str.split(' ', expand=True) #splits duration to int time and char min

	df[['Date','Start Hour']] = df['Meeting Start Time'].str.split(' ',expand=True)
	df[['End Date',"End Hour"]] = df['Meeting End Time'].str.split(' ',expand=True)

	df[['sHour', 'sMinute', 'sSecond']] = df['Start Hour'].str.split(':',expand=True)
	df[['eHour', 'eMinute', 'eSecond']] = df['End Hour'].str.split(':',expand=True)
	df = df.drop(columns=["Meeting Start Time","Meeting End Time"])

	df["sHour"] = df["sHour"].str.extract('(\d+)', expand=False).astype(int)
	df["sMinute"] = df["sMinute"].str.extract('(\d+)', expand=False).astype(int)
	df["eHour"] = df["eHour"].str.extract('(\d+)', expand=False).astype(int)
	df["eMinute"] = df["eMinute"].str.extract('(\d+)', expand=False).astype(int)

	df["Hour_diff"] = df["eHour"]-df["sHour"]
	df["Min_diff"] = df["eMinute"]-df["sMinute"]
	df["Session Duration"] = df["Hour_diff"]*60+df["Min_diff"]

	#Email is key. Combines emails and sums them by time.
	dropList = df.columns[:]
	dropList = dropList.drop(['Name', 'Attendee Email', 'Attendance Time', 'Session Duration', 'Date'])
	
	df = df.drop(columns=dropList)
	df["Date"] = df["Date"].str.extract('(\d+-\d+-\d+)', expand=False)

	df["Attendance Time"] = df["Attendance Time"].astype(int)
	df_grouped = df[['Attendee Email', 'Attendance Time']]
	df_grouped = df_grouped.groupby('Attendee Email').sum() #groups by email and sums their attendance time
	df = df.drop_duplicates(subset=['Attendee Email'])
	df = df.set_index('Attendee Email')

	df = df.sort_values(by=['Name'])
	df["Attendance Time"] = df_grouped["Attendance Time"]
	
	return df

for each in unique_files:
	df = pd.read_csv(cwd+"/"+unique_files[each], encoding="UTF-16LE", sep="\t")	
	df = pullRelData(df)
	##Attach new data to key data
	dateName = df["Date"][0]
	df_key[dateName] = df["Attendance Time"]

sumAllTimes = df_key.iloc[:,1:].sum(axis=1)
maxTimes = 4*60*(len(df_key.columns)-2)
df_key["Total Percentage"]  = sumAllTimes/maxTimes


df_key.to_csv(pth+"/Attendance.csv")

