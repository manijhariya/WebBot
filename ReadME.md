# WebBot for Data Collecting
A toolkit of scripts to automate the data collecting work which can again be
used in different Machine learning Project and other Projects..

# How ??
The goal is to write scripting building blocks that a human want to get from 
the different websites through search engines in place of their manual labour.
This means a fully-autonomous data collector, where a human has to give a word
or sentence at start and then it will go on and on to collect the data from all
over the websites. That a search engine can provide. It also going to add some
stratigacially word in the dictionary so that it can add word on and on..
There is also a small section of brute forcing the login websites for sometime
if possible.

Use can run individual scripts also by making some changes i have also commented 
out some dependent lines in script you can make changes and run individual file...

This project uses the data form [kaggle] which is used to add the word in dictionary
the comman names are taken from that database to avoid collecting data for particular
name.For bruetforce you have to get your own username and passwords file with names as [user_name.txt,passwords.txt]. Technically wanted to use the technical words only to collect the data. For that i have used my parameter in "wordSelector" file..

If you would like to run this code you need to first install Tor and set it to
work in 9055 port and take hashcode. Then install Privoxy and set it to work with
the tor.Also you need to add Stem and requests package from pip3 if already don't
these packages.You also see the guild to set up things in:
[view the gihub link to setup tor and privoxy]https://gist.github.com/DusanMadar/8d11026b7ce0bce6a67f7dd87b999f6b
[Download the names database]https://www.kaggle.com/new-york-city/nyc-baby-names 

# Files Structure
- **LinkCollection.py/** (To collect the link by search engine)
- **DataCollection.py/** (To collect the data from different websites) 
- **loginsetup.py/**     (To try to blind bruteforce in some websites if possible mostly on very light mode)
- **wordselector.py/**   (To select the word from different websites to add in dictionary)
- **Domain.py/**         (To always return the domain name to accessing the websites)
- **Main.py/**           (To maintain the run of the all scripts)

a work in progress by Manish...
