#!/bin/python3

"""
Created on Tue Feb 25 13:35:00 2020

@author: Manish
"""

from __future__ import print_function
from LinkCollection import formate
from urllib.request import urlopen
from bs4 import BeautifulSoup
from numpy import load,save
from time import sleep
from Main import logging
import urllib
import re
import os

parentdir =  os.getcwd()   #get the parent directory so that no reducance happens and control only on one directory

def loadessentials():   #loading all the essential files and to compare with the newkey
	try:
		d_names = []
		wordlist = []
		if os.path.isfile(parentdir+'/english_stop_word.npy') and os.path.isfile(parentdir+'/names.npy'):
			english_stop_word = load(parentdir+'/english_stop_word.npy')
			names = load(parentdir+'/names.npy')
			with open(parentdir+'/WordsDict.txt','r') as wd:
				word_list = wd.readlines()
			with open(parentdir+'/d_names.txt','r') as dn:
				dnames = dn.readlines()
			for word in word_list:
				wordlist.append(word.strip('\n\r'))
			for dname in dnames:
				d_names.append(dname.strip('\n\r'))
		else:
			names = []
			english_stop_word = []
			with open(parentdir+'/english_stop_word.txt','r') as esw:
				englishstopword = esw.readlines()
			with open(parentdir+'/names.txt','r') as n:
				comman_names = n.readlines()
			for word in englishstopword:
				english_stop_word.append(word.strip('\n\r'))
			for name in comman_names:
				names.append(name.strip('\r\n'))
			save(parentdir+'/english_stop_word.npy',english_stop_word)
			save(parentdir+'/names.npy',names)
			loadessentials()

	except FileNotFoundError:
		logging('T4Please get all the essential files first(english stop words,comman names)\n')

	return wordlist , d_names , english_stop_word , names

def words_processing(words):                                    #this one is trick part as we have to choice between the word
	wordlist,d_names,english_stop_word,names = loadessentials()  #i had to set the criteria for the word to get selected for which it is going to collecte the data in future data collecting 
	pattern = re.compile('\W')
	for word in words:
		word = word.lower()
		if not pattern.search(word):                             #1.criteria if word has special character it will be dropped
			word = re.sub('\s+',' ',word)                        #2.if it is present in the english stop word(most used word the ,i ,am etc.)
			word = re.sub('(?<=[.])\S+','',word)                 #3.if it is present in d_name (domain names)
			word = re.sub('[.]','',word)                         #4.if it is in most comman names to avoid collecting data about a person's name
			if (len(word.split(' '))) < 2:                       #5.last one if it is already in the wordlist itself
				if ((word not in english_stop_word) & (word not in d_names) & (word not in names) & (word not in wordlist)):
					with open(parentdir+'/WordsDict.txt','a') as w:
						w.write(word.lower()+'\n')
				else:
					continue
			else:
				newkey = ''
				for w in word.split(' '):
					if ((w not in english_stop_word) & (word not in d_names) & (word not in names) & (word not in wordlist)):
						newkey += w
						newkey += ' '
					else:
						continue
				newkey = newkey.strip(' ')
				with open(parentdir+'/WordsDict.txt','a') as w:
					w.write(newkey.lower()+'\n')

		else:
			continue

	return 0

def page_processing(html_text):                        #prcoessing page but this time i am using h1 to h6 html tag to get the head data and also titles
	words = []                                         # starting with the empty words and then collecting words from the html page as mentioned above.. 
	soup = BeautifulSoup(html_text,'lxml')
	for i in range(1,6):
		for wo in soup.find_all('h%d'%i):
			words.append(wo.get_text())
	words.append(soup.title.get_text())
	return words

def data_processing(lines,fi_le):
	for link in lines:
		link = link.strip('\r\n')
		format = formate(link)
		try:
			with (urlopen(format)) as f:
				html_text = f.read().decode('utf-8',errors='ignore')
				words = page_processing(html_text)
				words_processing(words)

		except urllib.error.HTTPError as e:
			logging("T4Didn't worked for:%s Error:%s\n"%(link,e),True)
			continue

		except urllib.error.URLError as e:
			logging('T4Bad URL:%s\n'%str(e),True)
			continue
	return 0

def link_processing(file_names):
	if file_names == []:
		logging('T4No files to process please check your link collection file\n')

	else:
		for fi_le in file_names:
			os.chdir(parentdir+'/data')
			with open(fi_le,'r') as f:
				lines = f.readlines()
			data_processing(lines,fi_le)
	return 0

def file():
	file_names = []
	if not os.path.isdir(parentdir+'/data'):
		logging('T4No Directory to process please check your link collection file\n')

	else:
		try:                                                 #same as in the DataCollection..
			os.chdir(parentdir+'/data')
			for a,b,c in os.walk(os.getcwd()):
				for fi_le in c:
					file_names.append(fi_le)
		except OSError:
			logging('Exception try as root:%s'%str(OSError))

	return link_processing(file_names)

def main():
	sleep(60)
	file()
	return 0
