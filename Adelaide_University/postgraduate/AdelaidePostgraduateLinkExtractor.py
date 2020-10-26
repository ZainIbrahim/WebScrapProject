from requests import get
from bs4 import BeautifulSoup
import time

'''Collect links'''

#get the first set of links
url = 'https://www.adelaide.edu.au/degree-finder/#pgrad-brse-tab'
request = get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(request.text, 'html.parser')
#print(soup.prettify())

links=[]
links2 =[]
div_tag = soup.find(id='pgrad-brse-tab')
for section in div_tag.find_all(class_='c-media-object__column'):
    narrow_down = section.find(class_='c-media-object__section c-media-object__section--content')
    if 'Study at Adelaide' not in narrow_down.h4.text:
        ul = narrow_down.find('ul')
        for li in ul.find_all('li'):
            link = li.a.get('href')
            print(link)
            links.append(link)

#get the second set of links
for x in range(len(links)):
    url2 = 'https://www.adelaide.edu.au'+links[x]
    request2 = get(url2)
    soup2 = BeautifulSoup(request2.text, 'html.parser')
    #print(soup2.prettify())

    for div_tag2 in soup2.find_all(class_='c-table'):
        table_tag = div_tag2.find('table')
        for tr in table_tag.find_all('tr'):
            link2 = tr.td.a.get('href')
            link2_complete = ('https://www.adelaide.edu.au/'+link2)
            print(link2_complete)
            links2.append(link2_complete)

with open('links.txt', 'w') as output:
    for row in links2:
        output.write(str(row)+'\n')
