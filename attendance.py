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


for each in unique_files:
	df = pd.read_csv(cwd+"/"+unique_files[each], encoding="UTF-16LE", sep="\t")	

	df[['Time','M']] = df['Attendance Duration'].str.split(' ', expand=True)

	df[['Date','Hour']] = df['Meeting Start Time'].str.split(' ',expand=True)

	df[['sHour', 'sMinute', 'sSecond']] = df['Hour'].str.split(':',expand=True)
	dropList = df.columns[:]
	dropList = dropList.drop(['Name', 'Time'])
	df["Time"] = df["Time"].astype(int)

	#df_grouped = df.groupby('Attendee Email')["Time"].sum()

	df_grouped = df.drop(columns=dropList)

	df_grouped = df.groupby('Name').sum()
	df_grouped.sort_values(by=['Name'])
	
	df_grouped.to_csv(pth+"/list_"+each)

