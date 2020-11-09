from requests import get
from bs4 import BeautifulSoup
import time

'''Collect links'''

links = []
links2 = []
links3 = []

#get the first set of links
url = 'https://www.tafesa.edu.au/'
request = get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'})
soup = BeautifulSoup(request.text, 'html.parser')
#print(soup.prettify())

ul_tag = soup.find('ul' , class_='dropdown-menu')
for li in ul_tag.find_all('li'):
    link = li.a.get('href')
    #print(link)
    links.append(link)
    if '/courses/primary-industries-science' in link:
        break


#get the second set of links
for x in range(len(links)):
    url2 = 'https://www.tafesa.edu.au'+links[x]
    request2 = get(url2, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'})
    soup2 = BeautifulSoup(request2.text, 'html.parser')
    #print(soup2.prettify())

    area_study = soup2.find(class_='areas_of_study')
    flex = soup2.find_all(class_='flex_item')
    for item in flex:
        link2 = item.a.get('href')
        #print(link2)
        links2.append(link2)

#get the third set of links
url3_ = None
for z in range(len(link2)):
    url3 = links2[z]
    if url3.startswith('/courses/'):
        url3_ = 'https://www.tafesa.edu.au'+links2[z]
    else:
        url3_ = links2[z]
    request3 = get(url3_, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'})
    soup3 = BeautifulSoup(request3.text, 'html.parser')
    #print(soup3.prettify())

    main_content = soup3.find(class_='mainContent study_area_course_list')
    table_tag = main_content.find_all('table')
    for table in table_tag:
        tr_tag = table.find_all('tr')
        for tr in table:
            link3 = tr.a.get('href')
            if link3.startswith('/xml/course/'):
                print(link3)
                links3.append(link3)
                links3 = list(dict.fromkeys(links3))



#write to file
with open('links.txt', 'w') as output:
    for row in links3:
        output.write(str(row)+'\n')

