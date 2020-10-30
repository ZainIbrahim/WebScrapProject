from requests import get
from bs4 import BeautifulSoup
import time

'''Collect links'''

links2 = []
links = []
#get the first set of links
url = 'https://www.vu.edu.au/study-at-vu/courses/browse-study-areas/all-courses-a-to-z'
request = get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'})
soup = BeautifulSoup(request.text, 'html.parser')
#print(soup.prettify())

div_tag = soup.find_all(class_='course-list-wrapper')[1]
ul_tag = div_tag.find_all('ul')
for ul in ul_tag:
    li_tag = ul.find_all('li')
    for li in li_tag:
        if "Bachelor" in li.text or "Diploma" in li.text:
            link = li.a.get('href')
            print(link)
            linkk = 'https://www.vu.edu.au'+link
            links.append(linkk)
print(len(links))


#write to file
with open('links.txt', 'w') as output:
    for row in links:
        output.write(str(row)+'\n')
