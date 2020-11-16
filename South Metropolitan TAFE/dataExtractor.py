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
        url = 'https://www.southmetrotafe.wa.edu.au'+line.replace('\n','')
        request = get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(request.text, 'html.parser')
        #print(soup.prettify())

        #get title
        if soup.find(class_='container c-page-title'):
            title = soup.find(class_='container c-page-title').text.strip()
            print(title)
            titles.append(title)
        else:
            skipped.append(url)
            continue

        #get level codes
        if "Certificate III" in title:
            code = "CERTIII"
        elif "Certificate II" in title:
            code = "CERTII"
        elif "Certificate I" in title:
            code = 'CERTI'
        elif "Advanced Diploma" in title:
            code = 'ADIP'
        elif "Bachelor" in title:
            code = 'BA'
        elif "Certificate IV" in title:
            code = 'CERTIV'
        elif "Diploma" in title:
            code = 'DIP'
        elif "Skill Set" in titles:
            code = "Skill Set"
        else:
            code = ''
        print(code)
        level_codes.append(code)

        #get description
        if soup.find(class_='field-item even'):
            div_tag = soup.find(class_='field-item even')
            p_tag = div_tag.find_next('p').text
            #print(p_tag)
            descriptions.append(p_tag)

        if len(titles) != len(descriptions):
            descriptions.append('')

        #durtation
        duration = ''
        dur2 = ''
        if soup.find('table' , class_='overview c-sms-overview'):
            table_tag = soup.find('table' , class_='overview c-sms-overview')
            if table_tag.find('tr'):
                tr_tag = table_tag.find_all('tr')
                for tr in tr_tag:
                    td_tag = tr.find('td')
                    if "Duration" in td_tag.text:
                        duration = td_tag.find_next('td').text.strip()
                        if "year" in duration:
                            dur1 = duration.split('y')
                            dur2 = dur1[0]
                            #print(dur2)
                            durations.append(dur2)
                        elif 'week' in duration:
                            dur1 = duration.split('w')
                            dur2= dur1[0]
                            #print(dur2)
                            durations.append(dur2)
                        elif 'day' in duration:
                            dur1 = duration.split('d')
                            dur2= dur1[0]
                            #print(dur2)
                            durations.append(dur2)
                        elif 'month' in duration:
                            dur1 = duration.split('m')
                            dur2= dur1[0]
                            #print(dur2)
                            durations.append(dur2)
                        elif 'semester' in duration:
                            dur1 = duration.split('sem')
                            dur2= dur1[0]
                            #print(dur2)
                            durations.append(dur2)

        if len(titles) != len(durations):
            durations.append('')

        #location
        if soup.find('table' , class_='overview c-sms-overview'):
            table_tag = soup.find('table' , class_='overview c-sms-overview')
            if table_tag.find('tr'):
                tr_tag = table_tag.find_all('tr')
                for tr in tr_tag:
                    td_tag = tr.find('td')
                    if "Where" in td_tag.text:
                        where = td_tag.find_next('td').text.strip()
                        #print(where)
                        cities.append(where)

        if len(titles) != len(cities):
            cities.append('')
        #faculty
        if soup.find(id='i-study-area'):
            faculty = soup.find(id='i-study-area').text
            #print(faculty)
            faculties.append(faculty)

        if len(titles) != len(faculties):
            faculties.append('')

        #course delivery mode
        if soup.find('table' , class_='overview c-sms-overview'):
            table_tag = soup.find('table' , class_='overview c-sms-overview')
            if table_tag.find('tr'):
                tr_tag = table_tag.find_all('tr')
                for tr in tr_tag:
                    td_tag = tr.find('td')
                    if "How" in td_tag.text:
                        how = td_tag.find_next('td').text.strip()

                        if 'Traineeship' in how:
                            course_delivery_mode = 'Traineeship'
                            course_delivery_modes.append(course_delivery_mode)
                            #print(course_delivery_mode)
                        elif 'Apprenticeship' in how:
                            course_delivery_mode = "Apprenticeship"
                            course_delivery_modes.append(course_delivery_mode)
                            #print(course_delivery_mode)

        if len(titles) != len(course_delivery_modes):
            course_delivery_modes.append('Normal')

        #career opportunities
        if soup.find('div', class_='job-opportunities'):
            job = soup.find('div', class_='job-opportunities')
            if job.find(class_='col-md-11 c-job-opportunities-option-container'):
                job_ = job.find(class_='col-md-11 c-job-opportunities-option-container').text.strip().replace('\n',', ')
                print(job_)
                career_outcomes.append(job_)

        if len(titles) != len(career_outcomes):
            career_outcomes.append('')

        #remarks
        remarks_renew = []
        if soup.find('table', class_='entrance_requirement'):
            entrance_req = soup.find('table', class_='entrance_requirement')
            if len(entrance_req.find_all('tbody')) > 1:
                tbody = entrance_req.find_all('tbody')[1]
                td_entrance = tbody.find_all('td')
                for td in td_entrance:
                    entrance = td.text
                    #print(entrance)
                    remarks_renew.append(entrance)
                remarks.append(' or '.join(remarks_renew))

        if len(titles) != len(remarks):
            remarks.append('')

        # set university name
        uni_name = 'South Metropolitan TAFE'
        uni_names.append(uni_name)

        # get local fees
        local_fees.append('')

        # set currency
        currencies.append('AUD')

        # set currency_time
        currency_times.append('Year')

        # set duration time
        if "year" in duration:
            if float(dur2) == 1:
                duration_times.append('Year')
            elif float(dur2) >1:
                duration_times.append('Years')
        elif "month" in duration:
            if float(dur2) == 1:
                duration_times.append('Month')
            elif float(dur2) >1:
                duration_times.append('Months')
        elif "week" in duration:
            if float(dur2) == 1:
                duration_times.append('Week')
            elif float(dur2) >1:
                duration_times.append('Weeks')
        elif "day" in duration:
            if float(dur2) == 1:
                duration_times.append('Day')
            elif float(dur2) >1:
                duration_times.append('Days')
        elif "semester" in duration:
            if float(dur2) == 1:
                duration_times.append('Semester')
            elif float(dur2) >1:
                duration_times.append('Semesters')
        else:
            duration_times.append('')

        # set fulltime
        #full_times.append('Yes')
        if soup.find('table' , class_='overview c-sms-overview'):
            table_tag = soup.find('table' , class_='overview c-sms-overview')
            if table_tag.find('tr'):
                tr_tag = table_tag.find_all('tr')
                for tr in tr_tag:
                    td_tag = tr.find('td')
                    if "How" in td_tag.text:
                        how = td_tag.find_next('td').text.strip()

                        if 'Part Time' in how:
                            part_time = 'Yes'
                            part_times.append(part_time)
                            #print('part time: ' + part_time)
                        elif 'Full Time' in how:
                            full_time = "Yes"
                            full_times.append(full_time)
                            #print('full time: ' +full_time)

        if len(titles) != len(part_times):
            part_times.append('')

        if len(titles) != len(full_times):
            full_times.append('')
        # set parttime
        #part_times.append('Yes')

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

        #prerequisite 1
        prere1s.append('')

        #prerequisite 1 grade
        prere1grades.append('')

        #free tafe
        free_tafes.append('No')

        #intfees
        int_fees.append('')


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
        #print('duration: ' + str(durations))


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

test_df.to_csv(r'/Users/zeinalabidin/desktop/CSV_files/South Metroplitan TAFE 201-391.csv', index=False,header=True)

for x in skipped:
    print('(skipped) ' + x)
