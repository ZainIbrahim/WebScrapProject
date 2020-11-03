from requests import get
from bs4 import BeautifulSoup
import time

'''Collect links'''

links2 = []
links = []
#get the first set of links
url = 'https://www.utas.edu.au/courses'
request = get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'})
soup = BeautifulSoup(request.text, 'html.parser')
#print(soup.prettify())

div_tag = soup.find(class_='g-row__flex g-row__gutter-sm g-row__pad-sm')
container = div_tag.find_all(class_='g-col g-col-global-2 g-col-md-4')
for x in container:
    if 'https://www.utas.edu.au/courses/study/' in x.a.get('href'):
        link = x.a.get('href')
        print(link)
        links.append(link)

#get the second set of links
for x in range(len(links)):
    url2 = links[x]
    request2 = get(url2, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'})
    soup2 = BeautifulSoup(request2.text, 'html.parser')
    #print(soup2.prettify())

    ul_tag = soup2.find_all(class_='list-item-link--list')
    for ul in ul_tag:
        li_tag = ul.find_all(class_='list-item-link--item')
        for li in li_tag:
            if 'Master' in li.find('a').text or 'Graduate Certificate' in li.find('a').text or 'Graduate Diploma' in li.find('a').text:
                if '/courses/' in li.find('a').get('href'):
                    a_tag = li.find('a').get('href')
                    a_tag2 = 'https://www.utas.edu.au' + a_tag
                    #print(a_tag)
                    links2.append(a_tag2)
                    links2 = list(dict.fromkeys(links2))

    print(links2)


#write to file
with open('links.txt', 'w') as output:
    for row in links2:
        output.write(str(row)+'\n')