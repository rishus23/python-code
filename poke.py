#!usr/bin/env/ python
# Python Script to automatically Poke people on facebook
# By Sebin Thomas
# USE AT YOUR OWN RISK
# It was written in a Hurry so no error handling whatsoever and there may be a zillion Bugs
# And it's not Safe 
# THOSE WHO USE THIS CODE ARE DOING SO IN THEIR OWN RISK AND THE AUTHOR 
# IS NOT ACCOUNTABLE FOR ANY DAMAGE WHATSOEVER
# Usage : poke.py Username password
import urllib2
import re
#import BeautifulSoup
from bs4 import BeautifulSoup
import sys

def login(user,pwd):
 loginReq=urllib2.Request("https://www.facebook.com/login.php?m=m&amp;refsrc=http%3A%2F%2Fm.facebook.com%2Findex.php&amp;refid=8","email=%s&pass=%s&login=Login"%(user,pwd))
 logconn=urllib2.urlopen(loginReq)
 data=BeautifulSoup.BeautifulSoup(logconn)
 #print data
 if "Log In" in data.head.title.string:
  return False
 else :
  return data


def main(arg):
 if arg<3:
  sys.exit("script should be called with your username and password")
 user=arg[1]
 pwd=arg[2]
 data=login(user,pwd)
 if not data==False:
  links=data.findAll('a')
  for a in links:
   url=a['href']
   if "/a/notifications.php?poke" in url:
    poke=urllib2.urlopen("http://m.facebook.com"+url)
    print "poked"

if __name__=="__main__":
 main(sys.argv)