#!/usr/bin/env python
# coding: utf-8

# --------------------------
import glob
import os
from os import walk
from os.path import isfile, join
import sys
# --------------------------
if (len(sys.argv) < 3):
	print("No argument was given or too few.\nUse: dirtree.py [path=] [recursive=yes/no]")
	sys.exit(1)

path = sys.argv[1]
recursive = sys.argv[2]
path = path+"/participant*.csv"
print(path)
f = []

if len(sys.argv) > 3:
	print("Too many arguments!")
	sys.exit(2)
elif not os.path.isdir(sys.argv[1]):
	print("Not a directory!")
	sys.exit(3)
#Recursive
if recursive=="True" or recursive=="true":
	for item in glob.glob(path, recursive=True):
		print(item)
		f.append(item)
#Non-Recursive
else:
	for item in glob.glob(path, recursive=False):
		print(item)
		f.append(item)
print(f)
sys.exit(0)

# -------
#Non Recursive

#	for (dirpath, dirnames, filenames) in walk(path):
#		f.extend(filenames)
#		print(f)
#		break

