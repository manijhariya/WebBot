#!/bin/python3

"""
Creted on Fri Feb 21 11:24:00 2020

@author: Manish
"""

from __future__ import print_function
from bs4 import BeautifulSoup
from urllib.request import urlopen
from Domain import dom
from time import sleep
from Main import logging
import os
import urllib
from LinkCollection import formate
import re

parentdir = os.getcwd()

def clean(para):                      #cleaning the paragrphas for the extra white spaces and useless tabs..
	cleaned = []
	for p in para:
		p = re.sub('\s+',' ',p)
		p = re.sub('\A\s','',p)
		cleaned.append(p)
	return cleaned

def writing_file(Dict):                 #writing to a file by processing it (cleaning and checking if done on this file) and 
	for domain,para in Dict.items():    # then writing paragraph by paragraph from the dictionary format
		if not domain in os.listdir():
			cleaned = clean(para)
			with open(domain,'w') as f:
				for line in cleaned:
					f.write(line+'\n')
		elif domain in os.listdir():
			with open(domain,'r') as f:
				lines = f.readlines()
			total_lines = len(lines)
			if total_lines < 100:
				cleaned = clean(para)
				if not total_lines == len(cleaned):
					with open(domain,'a') as f:
						f.write('\r-------Appending------\n')
						for line in cleaned:
							f.write(line+'\n')
				else:
					continue
			else:
				continue
		else:
			continue
	return 0

def file_processing(Dict,fi_le):            # some advanced and tricky file handling and in future usable files 
	fi_le = fi_le.replace('.txt','')
	try:
		os.chdir(parentdir)
	except OSError:
		logging('T2Try as root user %s\n'%str(OSError))
	try:
		if 'Datacollected' in os.listdir():
			os.chdir(parentdir+'/Datacollected')
		else:
			os.mkdir(parentdir+'/Datacollected')
			os.chdir(parentdir+'/Datacollected')
	except OSError:
		logging('T2Try as root user %s\n'%str(OSError))

	try:                               
		if file in os.listdir():
			os.chdir(parentdir+'/'+fi_le)
		else:
			os.mkdir(parentdir+'/'+fi_le)
			os.chdir(parentdir+'/'+fi_le)
	except OSError:
		logging('T2Try as root user%s\n'%str(OSError))

	writing_file(Dict)
	return 0

def page_processing(html_text):           # page prcessing and getting only the page paragraph element to save the collected data
	soup = BeautifulSoup(html_text,'html.parser')   
	para = []
	for pa in soup.find_all('p'):
		para.append(pa.get_text())
	return para

def data_processing(lines,fi_le):           # data processing fetching the html page from the server and then processing that particular page to get the useful data only
	Dict = {}                                  # making the dictionary for the collected data so they can be saved furthur
	for link in lines:
		link = link.strip('\r\n')
		format = formate(link)
		domain = dom(link)
		try:
			with (urlopen(format)) as f:
				html_text = f.read().decode('utf-8',errors='igonre')
				para = page_processing(html_text)
				Dict.update({domain:para})
		except urllib.error.HTTPError as e:               #except for the http error and logging them
			logging("T2Didn't Worked for:%s"%link+" Error::"+str(e)+"\n",True)
			continue

		except urllib.error.URLError as e:                #except for the bad urls and logging them 
			logging("T2Bad URL::" + str(e)+'\n',True)
			continue

	if not (Dict == {}):
		file_processing(Dict,fi_le)
	return 0

def link_processing(file_names):
	if file_names == []:                   #checking files is present if not simply back to main
		logging('T2No Files to process check if Link Collection file working!\n')

	else:
		for fi_le in file_names:
			os.chdir(parentdir+'/data')          #to work on the directory every link should be read and send to process
			with open(fi_le , 'r') as f:
				lines = f.readlines()
			data_processing(lines,fi_le)
	return 0

def file():
	file_names = []
	if not os.path.isdir(parentdir+"/data"):
		logging("T2No Directory to process please check link collection file\n")

	else:
		try:
			os.chdir(parentdir+'/data')         #checking if data is present to process
			for a,b,c in os.walk(os.getcwd()):
				for fi_le in c:
					file_names.append(fi_le)
		except OSError:                                   # if happpens check for any os error
			logging("T2Try as root user:%s\n"%str(OSError))

	return link_processing(file_names)

def main():
	sleep(60)               #to take a nap before start (link collection should take a run)
	file()
	return 0
