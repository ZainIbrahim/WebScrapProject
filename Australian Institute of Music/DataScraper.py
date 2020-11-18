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
        url = line.replace('\n','')
        request = get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(request.text, 'html.parser')
        #print(soup.prettify())

        #get title
        if soup.find(class_='gradient-course'):
            container = soup.find(class_='gradient-course')
            title = container.find_next('h3').text.strip()
            print(title)
            titles.append(title)
        else:
            skipped.append(url)
            continue

        #get level codes
        if "Bachelor" in title:
            code = 'BA'
        elif "Postgraduate" in title:
            code = 'MST'
        elif "Foundation" in title:
            code = 'FOUND'
        elif "Short Course" in titles or "Lessons" in titles:
            code = "Short Course"
        elif "Undergraduate Certificate" in titles:
            code = "GCERT"
        else:
            code = ''
        print(code)
        level_codes.append(code)

        #get duration
        if soup.find(class_='gradient-course'):
            container = soup.find(class_='gradient-course')
            table = container.find_next('table')
            tbody = table.find('tbody')
            for tr in tbody.find_all('tr'):
                th = tr.find('th')
                if 'Duration' in th.text:
                    duration = th.find_next('td').text
                    print(duration)
                    durations.append(duration)
        if len(titles) != len(durations):
            durations.append('')

        #get description
        if soup.find(class_='clearfix text-formatted field field--name-field-body-content-gt field--type-text-long field--label-hidden field__item'):
            desc = soup.find(class_='clearfix text-formatted field field--name-field-body-content-gt field--type-text-long field--label-hidden field__item')
            h3_tag = desc.find_next('h3').text
            print(h3_tag)
            descriptions.append(h3_tag)

        if len(titles) != len(descriptions):
            descriptions.append('')

        #location
        cities.append('Surry Hills')

        #faculty
        faculties.append('Music')

        #course delivery mode
        course_delivery_modes.append('Normal')

        #career opportunities
        career_renew =[]
        if soup.find(class_='careers'):
            career_possible = soup.find(class_='careers')
            for li in career_possible.find_all('li'):
                career = li.text
                career_renew.append(career)
                #print(career)
            career_outcomes.append(', '.join(career_renew))
            print(career_outcomes)

        if len(titles) != len(career_outcomes):
            career_outcomes.append('')

        #international students
        int_fees.append('')

        #remarks
        remarks.append('')

        # set university name
        uni_name = 'Australian Institute of Music'
        uni_names.append(uni_name)

        # get local fees
        local_fees.append('')

        # set currency
        currencies.append('AUD')

        # set currency_time
        currency_times.append('Year')

        # set duration time
        duration_times.append('Year')

        #set full time
        full_times.append('Yes')

        #set part time
        part_times.append('Yes')

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

        # prerequisite 1
        prere1s.append('')

        # prerequisite 1 grade
        prere1grades.append('')

        # free tafe
        free_tafes.append('No')

        print('Level code' + str(len(level_codes)))
        print('City' + str(len(cities)))
        print('Courses' + str(len(titles)))
        print('Faculty' + str(len(faculties)))
        print('full time' + str(len(full_times)))
        print('part time' + str(len(part_times)))
        print('Duration' + str(len(durations)))
        print('Description' + str(len(descriptions)))
        print('course delivery mode' + str(len(course_delivery_modes)))
        print('Career outcomes' + str(len(career_outcomes)))
        print('Remarks' + str(len(remarks)))
        print('skipped urls are: ' + str(skipped))

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

test_df.to_csv(r'/Users/zeinalabidin/desktop/CSV_files/Institute of Music 1.csv', index=False,header=True)

for x in skipped:
    print('(skipped) ' + x)
