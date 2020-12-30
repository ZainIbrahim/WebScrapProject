from requests import get
from bs4 import BeautifulSoup
import pandas as pd


url = 'https://www.kbs.edu.au/courses'
request = get(url)
soup = BeautifulSoup(request.text, 'html.parser')
#print(soup.prettify())

links = []
div_tag = soup.find_all(class_='view-content')[1]
for div_tag_ in div_tag.find_all(class_='views-row'):
    a_tag = div_tag_.a.get('href')
    print(a_tag)
    links.append(a_tag)

#write to file
with open('links.txt', 'w') as output:
    for row in links:
        output.write(str(row)+'\n')