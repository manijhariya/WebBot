#!/bin/python3

"""
Created on Thu Feb 20 17:23:00 2020

@author: Manish
"""

from __future__ import print_function
from bs4 import BeautifulSoup
from urllib.request import urlopen , Request
from random import choice
from time import sleep
from Main import logging,donewords
import os
import urllib
import re

parentdir = os.getcwd()          # getting parent directory to avoid any oserror's and misplacing any file 

def formate(fullurl):
	header_mozilla = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1)',
			'Accept': 'text/html.application/xhtml+xml,application/xml',
			'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			'Accept-Encoding': 'none',
			'Accept-language':'en-US,en;q=0.8',
			'Connection': 'keep-alive' }
	header_safari = {'User-Agent':'Mozilla/5.0 (iPhone;CPU iPhone OS 12_0 like Mac OS X)AppleWebKit/605.1.15 (KHTML,like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1',
			'Accept':'*/*',
			'Content-Type':'application/json',
			'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			'Accept-Encoding':'none',
			'Accept-language':'en-US,en;q=0.8',
			'Connection':'keep-alive' }
	header_chrome = {'User-Agent':'Mozilla/5.0 (Linux;Android 7.0;Pixel C Build/NRD90M;wv)AppleWebKit/537.36 (KHTML,like Gecko) Version/4.0 Chrome 52.0.2743.98 Safari/537.36',
			'Accept':'*/*',
			'Content-Type':'application/json',
			'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			'Accept-Encoding':'none',
			'Accept-language':'en-US,en;q=0.8',
			'Connection':'keep-alive' }
	header_opera = {'User-Agent':'Mozilla/5.0 (Linux;Android 7.0 HTC One M9 Build/MRA58LK) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.3',
			'Accept':'*/"',
			'Content-Type':'application/json',
			'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			'Accept-Encoding':'none',
			'Accept-language':'en-US,en;q=0.8',
			'Connection':'keep-alive' }
	header_flipkart = {'Host': '1.rome.api.flipkart.com',
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
			'Accept': '*/*',
			'Accept-Language': 'en-US,en;q=0.5',
			'Accept-Encoding': 'gzip, deflate, br',
			'Referer': 'https://www.flipkart.com/account/login?ret=%2Faccount%2F%3Frd%3D0%26link%3Dhome_account',
			'X-user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0 FKUA/website/42/website/Desktop',
			'Content-Type':'application/json',
			'Origin': 'https://www.flipkart.com',
			'Content-Length': '57',
			'Connection': 'keep-alive',
			'Pragma': 'no-cache',
			'Cache-Control': 'no-cache' }
	if not fullurl:                            #headers choice and return a different header for making a different requests i have used this function in others files also
		return choice((header_mozilla,header_safari,header_chrome,header_chrome,header_opera))
	else:                                      #returing the request object where i find the url othrewise header only see above 
		return  Request(url=fullurl,headers=header_mozilla)

def clean(links):
	usefullink = []
	pattern_google = re.compile("google")        #escaping any link with google because as a search engine i find that it mostly redirect on the links which it shows on the page
	for link in links:                           # links without google are the links which redirect the browser  
		if pattern_google.search(link):
			pass
		else:
			cleanedlink = re.sub('\A/url[?]q=','',link)
			if not cleanedlink == link:                          #cleaning the redirect or the part which brwosers simply ignore as the security check also
				cleanedlink = re.sub('(?<=&)\S+','',cleanedlink)
				cleanedlink = re.sub('&','',cleanedlink)
				usefullink.append(cleanedlink)
	return usefullink

def file_processing(links,w):
	if os.path.isfile(parentdir+'/data/%s.txt'%w):         #checking if the word done in past if so logging is done back to next word execution
		log = 'already exited data about:- %s\n'%w
		logging(log,True)
	else:
		try:
			with open(parentdir+'/data/%s.txt'%w,'w') as f:  #opening the file as the word itself and saving the links in that text file
				usefullink = clean(links)
				for link in usefullink:
					f.write(link+'\n')
		except FileNotFoundError:
			os.mkdir('data')
			file_processing(links,w)
	return 0

def page_processing(html_text,w):                   # opening every html page and get all the link parts to process furthur on the links
	soup = BeautifulSoup(html_text,'html.parser')
	links = []
	for link in soup.find_all('a'):
		links.append(link.get('href'))
	file_processing(links,w)
	return 0

def web(fullurl,w):
	format = formate(fullurl)
	try:
		with (urlopen(format)) as f:                              # opening every word in google to get processs in the (soup)
			html_text = f.read().decode('utf-8',errors='ignore')
			page_processing(html_text,w)
	except urllib.error.URLError:
		pass
	return 0

def full_url(escape):
	with open("WordsDict.txt",'r') as words:
		word = words.readlines()
	for i,w in enumerate(word):    
		if not i <= escape:           #escaping the already done lines for no repeating and optimisation
			w = w.strip('\r\n')
			w = re.sub('\s+','+',w)
			fullurl = "https://www.google.com/search?q={}".format(w)
			web(fullurl,w)
		else:
			continue
	donewords(len(word))       #returning the value to main no repentance
	return 0

def main(escape):
	sleep(1)
	full_url(escape)
