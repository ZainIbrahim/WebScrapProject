from requests import get
from bs4 import BeautifulSoup
import time
import pandas as pd

uni_names, country_names, titles, level_codes, descriptions, faculties, int_fees, currencies, cities, local_fees, skipped =([] for i in range(11))
currency_times, durations, duration_times, full_times, part_times, prere1s, prere2s, prere3s, prere1grades,prere2grades,prere3grades = ([] for i in range(11))
linksss, course_langs, availabilities,career_outcomes, onlines, offlines, distances, face_to_faces, blendeds, remarks, course_delivery_modes, free_tafes = ([] for i in range(12))

'''Collect data'''
with open('links.txt') as f:
    for line in f:

        #url = 'https://www.utas.edu.au/courses/s4a'
        url = 'https://sae.edu.au/'+line.replace('\n','')
        request = get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(request.text, 'html.parser')
        #print(soup.prettify())

        # get title
        if len(soup.find_all('div', class_='title-wrapper'))>1:
            div_title = soup.find_all('div', class_='title-wrapper')[1]
            title = div_title.h1.text
            print(title)
            titles.append(title)
        else:
            skipped.append(url)
            continue

        #description
        if soup.find('div', class_='overview-content scp'):
            div_desc = soup.find('div', class_='overview-content scp')
            desc = div_desc.p.text
            print(desc)
            descriptions.append(desc)

        if len(titles) != len(descriptions):
            descriptions.append('')

        #duration
        if soup.find('div', class_='content overview-tab'):
            div_overview = soup.find('div', class_='content overview-tab')
            if div_overview.find(class_='overview-right-wrapper'):
                div_wrapper = div_overview.find(class_='overview-right-wrapper')
                if div_wrapper.find('aside', class_='scp'):
                    div_aside = div_wrapper.find('aside', class_='scp')
                    for p in div_aside.find_all('p'):
                        if 'Year' in p.text or 'MTHS' in p.text or 'Week' in p.text or 'Trimester' in p.text:
                            duration = p.text
                            print(duration)
                            durations.append(duration)
                            break

        if len(titles) != len(durations):
            durations.append('')

        #level code
        if "Bachelor" in title:
            level_codes.append('BA')
        elif "Master" in title:
            level_codes.append('MST')
        elif "Associate Degree" in title:
            level_codes.append('ADEG')
        elif "Diploma" in title:
            level_codes.append('DIP')
        elif "Certificate III" in title:
            level_codes.append('CERTIII')
        elif 'Short Course'  in title:
            level_codes.append('Short Course')
        elif 'Undergraduate' in title:
            level_codes.append('UCERT')
        elif 'Graduate'in title:
            level_codes.append('GCERT')
        else:
            level_codes.append('')

        #international fees
        int_fees.append('')

        #get city
        cities_renew = []
        if soup.find('div', class_='content overview-tab'):
            div_overview = soup.find('div', class_='content overview-tab')
            if div_overview.find(class_='overview-right-wrapper'):
                div_wrapper = div_overview.find(class_='overview-right-wrapper')
                ul_tag = div_wrapper.find('ul')
                for li in ul_tag.find_all('li'):
                    city = li.text
                    cities_renew.append(city)
                cities.append(', '.join(cities_renew))
                print(cities)
        if len(titles) != len(cities):
            cities.append('')

        #get career options
        career_outcomes_renew = []
        h2_tag = soup.find_all('h2')
        for h2 in h2_tag:
            if 'Career Options' in h2.text:
                ul_tag = h2.find_next('ul')
                for li in ul_tag.find_all('li'):
                    career = li.text
                    career_outcomes_renew.append(career)
                career_outcomes.append(', '.join(career_outcomes_renew))
                print(career_outcomes)

        if len(titles) != len(career_outcomes):
            career_outcomes.append('')

        #prerequisite 1
        prere1s_renew = []
        h3_tag = soup.find_all('h3')
        for h3 in h3_tag:
            if 'Entry requirements' in h3.text:
                if h3.find_next('ol'):
                    ol = h3.find_next('ol')
                    for li in ol.find_all('li'):
                        pre = li.text
                        prere1s_renew.append(pre)
                    prere1s.append(', '.join(prere1s_renew))
                    print(prere1s)

        if len(titles) != len(prere1s):
           prere1s.append('')

        #faculty
        if 'animation' in url:
            faculties.append('Animation')
        elif 'audio' in url:
            faculties.append('Audio')
        elif 'design' in url:
            faculties.append('Design')
        elif 'film' in url:
            faculties.append('Film')
        elif 'games' in url:
            faculties.append('Games')
        elif 'web-and-mobile' in url:
            faculties.append('Web and Mobile')
        else:
            faculties.append('')

        #course delivery mode
        course_delivery_modes.append('Normal')

        #remarks
        remarks.append('')

        # set university name
        uni_name = 'SAE Institute'
        uni_names.append(uni_name)

        # get local fees
        local_fees.append('')

        # set currency
        currencies.append('AUD')

        # set currency_time
        currency_times.append('Year')

        #set duration time
        duration_times.append('Year')

        #full time
        full_times.append('Yes')

        #part time
        part_times.append('NO')

        # set prerequisite 2
        prere2s.append('')

        # set prerequisite 3
        prere3s.append('')

        # set prerequisite 2 grade
        prere2grades.append('')

        # set prerequisite 3 grade
        prere3grades.append('')

        # set website
        linksss.append(url)

        # set course language
        course_langs.append('English')

        # get availability
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

        # prerequisite 1 grade
        prere1grades.append('')

        # free tafe
        free_tafes.append('No')

        print('City: ' + str(len(cities)))
        print('Courses: ' + str(len(titles)))
        print('Faculty: ' + str(len(faculties)))
        print('Duration: ' + str(len(durations)))
        print('Description: ' + str(len(descriptions)))
        print('Career outcomes: ' + str(len(career_outcomes)))
        print('prerequisite1: ' + str(len(prere1s)))

        print('skipped urls are: ' + str(skipped))
        # print('duration: ' + str(durations))

        print('====================================================================================================================')
        time.sleep(1.5)

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
    'Remarks': remarks,
    'Course delivery mode': course_delivery_modes,
    'Free TAFE': free_tafes
})

test_df.to_csv(r'/Users/zeinalabidin/desktop/CSV_files/SAE Institute 1.csv', index=False,
               header=True)

for x in skipped:
    print('(skipped) ' + x)