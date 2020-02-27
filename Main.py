#!/bin/python3

"""
Created on Web Feb 25 9:35:00 2020

@author: Manish
"""

import os
import sys
import time
from threading import Thread

parentdir = os.getcwd()                    #getting the parent directory so that script doesn't get lost in the space

def logging(message,flag=False):            #logging function called from every file to keep the logging in txt mode
	with open(parentdir+'/logs.txt','a') as l:
		l.write(str(time.ctime(time.time())+'::'+message))
	if not flag:
		print ('%s:Exception happened please look for it in currentdir/log.txt file'%str(time.ctime(time.time())))
		sys.exit()
	else:
		return 0
def donewords(escape = -1):
	return escape

try:                                            #checking if all the files present in the same directory or not
	import DataCollection
	import LinkCollection
	import loginsetup
	import wordselector
	import Domain
except ImportError:
	logging("Since u don't have enough files. You can't run this program\n")

if (os.system('service tor start') and os.system('service privoxy start')):  #starting the privoxy and tor if present
	logging('Please check your privoxy and tor to run this program\n')
else:
	pass

def f1(name):
	print (str(name)+'::'+str(time.ctime(time.time())))
	return 0

def startprogram():
	escape = donewords()                                     #it will give the wordDict done lines to process faster
	t1 = Thread(target=LinkCollection.main,args=(escape,))  #LinkCollection Thread
	t2 = Thread(target=DataCollection.main)                 #DataCollection Thread
	t3 = Thread(target=loginsetup.main)                     #loginsetup Thread               
	t4 = Thread(target=wordselector.main)                   #wordselector Thread
	t1.start()
	t2.start()
	t3.start()
	t4.start()
	t1.join()
	t2.join()
	t3.join()
	t4.join()
	return 0

def main():
	startprogram()
	time.sleep(5)                                  #take a nap to give a break to the processor..
	return 0

if __name__ == '__main__':
	main()
