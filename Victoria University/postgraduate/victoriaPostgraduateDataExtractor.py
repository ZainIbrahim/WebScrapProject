from requests import get
from bs4 import BeautifulSoup
import time
import pandas as pd

uni_names, country_names, titles, level_codes, descriptions, faculties, int_fees, currencies, cities, local_fees, skipped =([] for i in range(11))
currency_times, durations, duration_times, full_times, part_times, prere1s, prere2s, prere3s, prere1grades,prere2grades,prere3grades = ([] for i in range(11))
linksss, course_langs, availabilities,career_outcomes, onlines, offlines, distances, face_to_faces, blendeds, remarks = ([] for i in range(10))

'''Collect data'''
#with open('links.txt') as f:
#    for line in f:

url = 'https://www.vu.edu.au/courses/international/NMIT'
#url = line
request = get(url,headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'})
soup = BeautifulSoup(request.text, 'html.parser')
#print(soup.prettify())

#get title
if soup.find(class_='page-header'):
    title = soup.find(class_='page-header').text
    print(title)
    titles.append(title)
else:
    #pass
    skipped.append(url)
    #continue

#get duration
duration = None
if soup.find(class_='block block-ds-extras container content fields-5 clearfix'):
    section_tag = soup.find(class_='block block-ds-extras container content fields-5 clearfix')
    #print(section_tag)
    div_tag = section_tag.find_all(class_='field-course-essentials col-md-3 col-sm-6')
    if div_tag !=0:
        for div in div_tag:
            if "Duration" in div.find('strong').text:
                dur = div.find_next('div').text
                dur2 = dur.split('Duration:')
                dur3 = dur2[1].split('year')
                duration = dur3[0].strip()
                print(duration)
                durations.append(duration)

if len(titles)!=len(durations):
    durations.append('')

#get international fees
if soup.find(class_='block block-ds-extras container content fields-5 clearfix'):
    section_tag = soup.find(class_='block block-ds-extras container content fields-5 clearfix')
    #print(section_tag)
    div_tag = section_tag.find_all(class_='field-course-essentials col-md-3 col-sm-6')
    if div_tag !=0:
        for div in div_tag:
            if "Fees" in div.find('strong').text:
                fe = div.find_next('div').text
                fe1 = fe.split('$')
                fe2 = fe1[1].split('*')
                fe3 = fe2[0].strip()
                print(fe3)
                int_fees.append(fe3)

if len(titles)!=len(int_fees):
    int_fees.append('')

#get city
if soup.find(class_='block block-ds-extras container content fields-5 clearfix'):
    section_tag = soup.find(class_='block block-ds-extras container content fields-5 clearfix')
    #print(section_tag)
    div_tag = section_tag.find_all(class_='field-course-essentials col-md-3 col-sm-6')
    if div_tag !=0:
        for div in div_tag:
            if "Location" in div.find('strong').text:
                city = div.find_next('div').text
                city1= city.split('Location:')
                city2=  city1[1].strip()
                print(city2)
                cities.append(city2)

if len(titles)!=len(cities):
    cities.append('')

#get description
descriptions_renew = []
if soup.find(class_='paragraph--lead'):
    p_tag = soup.find(class_='paragraph--lead')
    p_tagg = soup.find(class_='paragraph--lead').text
    print(p_tagg)
    descriptions_renew.append(p_tagg)
    if p_tag.find_next('div', class_='field-item even'):
        other_ptags= p_tag.find_next('div', class_='field-item even')
        p_tagg2 = other_ptags.find_all('p')
        if len(p_tagg2)>2:
            for p in p_tagg2[:2]:
                desc = p.text
                print(desc)
                descriptions_renew.append(desc)
            descriptions.append(' '.join(descriptions_renew))

if len(titles)!=len(descriptions):
    descriptions.append('')

#get careers
career_outcomes_renew = []
if soup.find(id='careers'):
    div_tag2 = soup.find(id='careers')
    if div_tag2.find('ul'):
        ul_tag = div_tag2.find('ul')
        li_tag = ul_tag.find_all('li')
        if li_tag!=0:
            for li in li_tag:
                career = li.text
                #print(career)
                career_outcomes_renew.append(career)
            career_outcomes.append('/ '.join(career_outcomes_renew))
            print(career_outcomes)
    else:
        if div_tag2.find('p'):
            career = div_tag2.find('p')
            career_outcomes.append(career)

if len(titles)!=len(career_outcomes):
    career_outcomes.append('')


#set prerequisite 1
if soup.find_all('h3'):
    h3_tag = soup.find_all('h3')
    for h3 in h3_tag:
        if 'Entry requirements' in h3.text:
            text = h3.find_next('p')
            if "IELTS" in text.text:
                prerequisite1 = 'IELTS'
                print(prerequisite1)
                prere1s.append(prerequisite1)

if len(titles)!=len(prere1s):
    prere1s.append('')

#prerequisite 1 grade
if soup.find_all('h3'):
    h3_tag = soup.find_all('h3')
    for h3 in h3_tag:
        if 'Entry requirements' in h3.text:
            text = h3.find_next('p')
            if "IELTS" in text.text:
                try:
                    pre2a = text.text.split('Overall score or')
                    pre2b = pre2a[1].split('(')
                    pre2c = pre2b[0].strip()
                    print(pre2c)
                    prere1grades.append(pre2c)
                except:
                    try:
                        pre2a = text.text.split('Overall score of')
                        pre2b = pre2a[1].split('(')
                        pre2c = pre2b[0].strip()
                        print(pre2c)
                        prere1grades.append(pre2c)
                    except:
                        pre2a = text.text.split('IELTS')
                        pre2b = pre2a[1].split('or')
                        pre2c = pre2b[0].strip()
                        print(pre2c)
                        prere1grades.append(pre2c)
if len(titles)!=len(prere1grades):
    prere1grades.append('')

#set level code
if "Certificate IV" in title:
    code = "CERTIV"
elif "Certificate I" in title:
    code = "CERTI"
elif "Certificate II" in title:
    code = "CERTII"
elif "Certificate III" in title:
    code = "CERTIII"
elif "Master" in title:
    code = "MST"
elif "Victorian Certificate" in title:
    code = "Victorian Certificate"
elif "Graduate Diploma" in title:
    code = "GDIP"
elif "Advanced Diploma" in title:
    code = "ADIP"
elif "Graduate Certificate" in title:
    code = "GCERT"
else:
    code = ''
print(code)
level_codes.append(code)

#get faculty
if soup.find(class_='field field-name-field-college field-type-link-field field-label-inline clearfix'):
    div_tag3 = soup.find(class_='field field-name-field-college field-type-link-field field-label-inline clearfix')
    if div_tag3.a:
        faculty = div_tag3.a.text
        print(faculty)
        faculties.append(faculty)

if len(titles)!=len(faculties):
    faculties.append('')

# set university name
uni_name = 'Victoria University'
uni_names.append(uni_name)

# get local fees
local_fees.append('')

# set currency
currencies.append('AUD')

# set currency_time
currency_times.append('Year')

# set duration time
if duration is not None:
    if float(duration) == 1.0:
        duration_times.append('Year')
    elif float(duration) > 1:
        duration_times.append('Years')

if len(duration_times) != len(titles):
    duration_times.append('Year')

# set fulltime
full_times.append('Yes')

# set parttime
part_times.append('Yes')

#set prerequisite 2
prere2s.append('')

#set prerequisite 3
prere3s.append('')


#set prerequisite 2 grade
prere2grades.append('')

#set prerequisite 3 grade
prere3grades.append('')

#set website
linksss.append(url)

#set course language
course_langs.append('English')

#get availability
availabilities.append('A')

# set country
country_names.append('Australia')

# online
online = 'Yes'
onlines.append(online)

# offline
offline = 'Yes'
offlines.append(offline)

# distance
distances.append('')

# face-to-face
if offline is 'Yes':
    face_to_faces.append('Yes')
else:
    face_to_faces.append('NO')

# blended
if online and offline == 'Yes':
    blendeds.append('Yes')
else:
    blendeds.append("NO")

#remarks
remarks.append('')


print('Level code' + str(len(level_codes)))
print('City' + str(len(cities)))
print('Courses' + str(len(titles)))
print('Faculty' + str(len(faculties)))
print('Int fees' + str(len(int_fees)))
print('Duration' + str(len(durations)))
print('Prerequiste_1' + str(len(prere1s)))
print('Website' + str(len(linksss)))
print('Description' + str(len(descriptions)))
print('Career outcomes' + str(len(career_outcomes)))
print('Remarks' + str(len(remarks)))
print('skipped urls are: '+str(skipped))
print('====================================================================================================================')

test_df = pd.DataFrame({
    'Level code': level_codes,
    'University': uni_names,
    'City': cities,
    'Courses': titles,
    'Faculty': faculties,
    'Int fees': int_fees,
    'Local fees': local_fees,
    'Currency': currencies,
    'Currency Time': currency_times,
    'Duration': durations,
    'Duration Time': duration_times,
    'Prerequiste_1': prere1s,
    'Prerequiste_2': prere2s,
    'Prerequiste_3': prere3s,
    'Prerequiste_1_grade': prere1grades,
    'Prerequiste_2_grade': prere2grades,
    'Prerequiste_3_grade': prere3grades,
    'Website': linksss,
    'course_lang': course_langs,
    'Availability': availabilities,
    'Description': descriptions,
    'Career outcomes': career_outcomes,
    'Country': country_names,
    'Online': onlines,
    'Offline': offlines,
    'Distance': distances,
    'Face to face': face_to_faces,
    'Blended': blendeds,
    'Remarks': remarks
})

test_df.to_csv(r'/Users/zeinalabidin/desktop/CSV_files/VictoriaUniversityPostgraduateCourses1.csv', index=False,header=True)

for x in skipped:
    print(x)