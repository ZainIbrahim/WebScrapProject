from requests import get
from bs4 import BeautifulSoup
import time

'''Collect links'''
#get the first set of links
url = 'https://study.curtin.edu.au/study-areas/'
request = get(url)
soup = BeautifulSoup(request.text, 'html.parser')
#print(soup.prettify())

links=[]
all_links=[]
for div_tag in soup.find_all(class_='card card--image'):
    ul_tag = div_tag.find(class_='link-list link-list--magenta pink-links')
    li_tag = ul_tag.find_all('li')[1]
    a_tag = li_tag.a.get('href')
    #print(a_tag)
    links.append(a_tag)

#get the second set of links
for j in range(len(links)):
    url2 = links[j]
    request2 = get(url2)
    soup2 = BeautifulSoup(request2.text, 'html.parser')
    #print(soup2.prettify())

    pagination_tag = soup2.find(class_='search-pagination__pages')
    pagination = pagination_tag.find_all('a')
    links2 = []
    for a in pagination:
        page_url = a.get('href')
        page = ('https://study.curtin.edu.au'+page_url)
        #print(page)
        links2.append(page)

    for z in range(len(links2)):
        url3 = links2[z]
        request3 = get(url3)
        soup3 = BeautifulSoup(request3.text, 'html.parser')
        #print(soup3.prettify())

        data = soup3.find(class_='search-results__card-container')
        for x in data.find_all(class_='search-card'):
            link = x.a.get('href')
            print(link)
            all_links.append(link)

    time.sleep(5)

with open("file.txt", "w") as output:
    for row in all_links:
        output.write(str(row) + '\n')
    #output.write(str(all_links))

