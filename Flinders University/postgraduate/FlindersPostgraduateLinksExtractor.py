from requests import get
from bs4 import BeautifulSoup
import time

'''Collect links'''
links2 = []
links = []
#get the first set of links
url = 'https://www.flinders.edu.au/study/courses'
request = get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(request.text, 'html.parser')
#print(soup.prettify())
section_wrapper = soup.find_all(class_='component_in_section_wrapper')[9:14]
for ct in section_wrapper:
    for cta_button in ct.find_all(class_='cta-button'):
        a_tag = cta_button.find('a').get('href')
        print(a_tag)
        links.append(a_tag)

#get the second set of links
for x in range(len(links)):
    url2 = 'https://www.flinders.edu.au' +links[x]
    #url2 = 'https://www.flinders.edu.au/international/science'
    request2 = get(url2)
    soup2 = BeautifulSoup(request2.text, 'html.parser')
    #print(soup2.prettify())

    item_content = soup2.find_all(class_='item_content')
    for item in item_content:
        li_tag= item.ul.find_all('li')
        for li in li_tag:
            if 'https://www.flinders.edu.au/study/courses/postgraduate' in li.a.get('href'):
                link2 = li.a.get('href')
                print(link2)
                links2.append(link2)


#write to file
with open('links.txt', 'w') as output:
    for row in links2:
        output.write(str(row)+'\n')
