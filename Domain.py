#!/bin/python3

"""
Created on Unknown Feb 2020

@author: Manish
"""

import re

def dom(url):
	domain = re.sub('\Ahttp://|\Ahttps://','',url)
	domain = re.sub('\Awww.','',domain)
	domain = re.sub('\A[.]','',domain)
	domain = re.sub('(?<=/)\S+','',domain)
	domain = re.sub('/','.txt',domain)
	return (domain.lower())

def domname(url):
	domain = re.sub('\Ahttp://|\Ahttps://','',url)
	domain = re.sub('(?<=/)\S+','',domain)
	if re.search('\Awww.',domain):
		domain = re.sub('\Awww.','',domain)
		domain = re.sub('\A[.]','',domain)
		domain = re.sub('(?<=[.])\S+','',domain)
	else:
		domain = re.search('(?<=[.])\S+',domain)
		domain = re.sub('(?<=[.])\S+','',domain.group(0))
	domain = re.sub('[.]','',domain)
	return (domain.lower())

