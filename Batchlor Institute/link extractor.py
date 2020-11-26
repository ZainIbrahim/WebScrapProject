from requests import get
from bs4 import BeautifulSoup
import time

'''Collect links'''

links = []
links2 = []
links3 = []

#get the first set of links
url = 'https://www.batchelor.edu.au/students/courses/vet-courses/'
request = get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'})
soup = BeautifulSoup(request.text, 'html.parser')
#print(soup.prettify())

div_tag = soup.find_all(class_='shortcode-list shortcode-list-bullet2')
for div in div_tag:
    ul_tag = div.find('ul')
    li_tag = ul_tag.find_all('li')
    for li in li_tag:
        #if li.find('a').get('href'):
        #print(li)
        link = li.find('a')
        if link:
            link_ = link.get('href')
            print(link_)
            links.append(link_)


#write to file
with open('links.txt', 'w') as output:
    for row in links:
        output.write(str(row)+'\n')