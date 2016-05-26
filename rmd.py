import requests
import datetime
from bs4 import BeautifulSoup as bs
from lxml import html
url = 'http://www.realmadrid.com/en/football/schedule'
response = requests.get(url)
html = response.content
soup = bs(html)
opp = soup.find('div', {'class': 'm_highlighted_next_game_team m_highlighted_next_game_second_team'}).strong.contents
time = soup.find('div', {'class': 'm_highlighted_next_game_info_wrapper'}).time.contents
date = soup.find('header', {'class': 'm_highlighted_next_game_header'}).time.contents
time1 = time[0]
hour=int(time1[:2])
date1 = date[0]
year=int(date1[:4])
month=date1[5:7]
if '0' in month:
    month=month[-1:]
month=int(month)
day=int(date1[-2:])
print("Real Madrid is playing",opp[0],"at",time1[:-1],"on",date[0])
import time
def countdown(t):
    while t:
        min1, secs = divmod(t, 60)
        hours1, mins = divmod(min1,60)
        days, hours = divmod(hours1, 24)
        timeformat = '{:02d} days {:02d}:{:02d}:{:02d}'.format(days,hours, mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1
    print('Enjoy the match!')
start = datetime.datetime.now()
end = datetime.datetime(year=year, month=month, day=day, hour=hour)
diff = end - start
countdown(int(diff.total_seconds()))
