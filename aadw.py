#Owner : Vinay Chandran
#Company : IntelliDesigns
#Created : April 10, 2016, 3:05AM IST
#Name : AlbumArtDownloader
#Version : 1.0

import os
import time
import requests
from tabulate import tabulate
import urllib
import lxml.html
from bs4 import BeautifulSoup as bs


def listArtists():
    baseURL="https://en.wikipedia.org/wiki/Category:Album_covers_by_recording_artist"
    basePage = urllib.urlopen(baseURL)
    baseDom =  lxml.html.fromstring(basePage.read())
    q=[]
    r=[]
    for link in baseDom.xpath('//a/@href'):
        if(link[6:14].lower()=='category'):
            q.append(link)
    q=q[1:-6]
    for i,name in enumerate(q):
        name = name[15:-13]
        name=name.split('_')
        name=' '.join(name)
        r.append(name)
    table=[[str(i+1),r[i]]for i in range(len(q))]
    print tabulate(table,headers=['No','Artist Name'])
    return q,r

def fetchImages(q,r,choice):
    print 'Downloading album arts of '+'\033[1m\033[32m'+r[int(choice)]+'\033[0m'
    url='https://en.wikipedia.org'+q[int(choice)]
    mainPage = urllib.urlopen(url)
    mainDom =  lxml.html.fromstring(mainPage.read())
    s=[]
    t=[]
    for link in mainDom.xpath('//a/@href'):
        if (link[-3:].lower()=='jpg' or link[-3:].lower()=='png' or link[-3:].lower()=='jpeg'):
            link='https://en.wikipedia.org'+link
            s.append(link)

    for url in s:
        response = requests.get(url)
        html = response.content
        soup = bs(html,"lxml")
        link2 = soup.find('div', {'class': 'fullImageLink'}).a
        url2='http:'+link2['href']
        filename=url2.rsplit('/',1)[1]
        sd = os.path.dirname(__file__)
        sdsd = os.path.join(sd, r[int(choice)])
        if not os.path.exists(sdsd):
            os.mkdir(sdsd)
        fullfilename = os.path.join(sdsd, filename)
        urllib.urlretrieve(url2, fullfilename)
    print 'Download '+'\033[1m\033[32m'+'complete!'+'\033[0m'

def menu():
    print
    print 'Album arts downloader by'+'\033[1m\033[32m' +' IntelliDesigns'+'\033[0m'
    time.sleep(1)
    print 'List of artist will be printed shortly. Enter the number to download the corresponding artist cover arts'
    time.sleep(1)
    q,r=listArtists()
    time.sleep(0)
    choice=raw_input('Enter the no. corresponding to the artist name : ')
    fetchImages(q,r,int(choice)-1)
menu()
