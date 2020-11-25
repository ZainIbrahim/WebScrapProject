from bs4 import BeautifulSoup
from requests import get


url = get('https://sae.edu.au/courses/')
soup = BeautifulSoup(url.text, 'html.parser')
#print(soup.prettify())

links = []
'''collect links'''

div_tag = soup.find('div', class_='course-panel-wrapper')
for li_tag in div_tag.find_all('a'):
    link = li_tag.get('href')
    print(link)
    links.append(link)


#write to file
with open('links.txt', 'w') as output:
    for row in links:
        output.write(str(row)+'\n')