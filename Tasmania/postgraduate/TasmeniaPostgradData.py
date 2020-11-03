from requests import get
from bs4 import BeautifulSoup
import time
import pandas as pd

uni_names, country_names, titles, level_codes, descriptions, faculties, int_fees, currencies, cities, local_fees, skipped =([] for i in range(11))
currency_times, durations, duration_times, full_times, part_times, prere1s, prere2s, prere3s, prere1grades,prere2grades,prere3grades = ([] for i in range(11))
linksss, course_langs, availabilities,career_outcomes, onlines, offlines, distances, face_to_faces, blendeds, remarks = ([] for i in range(10))

'''Collect data'''
with open('links.txt') as f:
    for line in f:

        #url = 'https://www.utas.edu.au/courses/s4a'
        url = line.replace('\n','')
        request = get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(request.text, 'html.parser')
        #print(soup.prettify())

        #get title
        if soup.find(class_='l-object-page-header--page-title'):
            title = soup.find(class_='l-object-page-header--page-title').text
            print(title)
            titles.append(title)
        else:
            skipped.append(url)
            continue

        #get duration
        dur_3 = None
        duration_and_location = soup.find(class_='g-row g-row__pad-sm')
        for div in duration_and_location.find_all(class_='g-col g-col-global-1-1 g-col-sm-1-1 g-col-md-1-3'):
            if 'Duration' in div.h3.text:
                duration = div.dd.text
                if 'Year' in duration:
                    dur_1 = duration.split('Year')
                    if dur_1[0].split('Minimum'):
                        dur_2 = dur_1[0].split('Minimum')
                        dur_3 = dur_2[1].strip()
                        print(dur_3)
                        durations.append(dur_3)
                    else:
                        dur_2 = dur_1[0]
                        print(dur_2)
                        durations.append(dur_2)

        if len(titles) != len(durations):
            durations.append('')

        #get location
        for div in duration_and_location.find_all(class_='g-col g-col-global-1-1 g-col-sm-1-1 g-col-md-1-3'):
            if 'Location' in div.h3.text:
                h3_tag = div.h3
                if h3_tag.find_next('dt'):
                    campus = h3_tag.find_next('dt').text
                    print(campus)
                    cities.append(campus)

        if len(titles) != len(cities):
            cities.append('Hobart')


        #get international fees
        p_tag = soup.find_all('p')
        for p in p_tag:
            if "Total Course Fee (international students)" in p.text:
                if "TBA" not in p.text:
                    fees = p.text
                    fee1 = p.text.split('$')
                    fee2= fee1[1].split('AUD')
                    fee3= fee2[0].strip()
                    print(fee3)
                    int_fees.append(fee3)

        if len(titles) != len(int_fees):
            int_fees.append('')

        #get description
        descriptions_renew = []
        h4_tag = soup.find_all('h4')
        for h4 in h4_tag:
            
            if 'Course objectives' in h4.text:
                if h4.find_next(class_='richtext richtext__medium'):
                    if h4.find_next(class_='richtext richtext__medium'):
                        desc = h4.find_next(class_='richtext richtext__medium')
                        if desc.p:
                            desc1 = desc.p.text
                            print(desc1)
                            descriptions.append(desc1)
        if len(titles) != len(descriptions):
            if len(soup.find_all(class_='lede')) >1:
                div = soup.find_all(class_='lede')[1].text
                print(div)
                descriptions.append(div)

        if len(titles) != len(descriptions):
            descriptions.append('')

        #get career outcomes
        h2_tag = soup.find_all('h2')
        for h2 in h2_tag:
            if 'Career outcomes' in h2.text:
                if h2.find_next('p'):
                    career = h2.find_next('p').text
                    print(career)
                    career_outcomes.append(career)

        if len(titles) != len(career_outcomes):
            career_outcomes.append('')



        #get prerequisite 1
        requisite1 = soup.find_all('p')
        for p in requisite1:
            if 'International students must provide an IELTS' in p.text:
                print('IELTS')
                prere1s.append('IELTS')

        if len(titles) != len(prere1s):
            prere1s.append('')

        #get prerequisite 1 grade
        for p in requisite1:
            if 'test score of at least Band' in p.text:
                grade1 = p.text
                if 'with a minimum of' in grade1:
                    grade2 = grade1.split("with a minimum of")
                    grade3 = grade2[1].split('.')
                    grade4 = grade3[0].strip()
                    print(grade4)
                    prere1grades.append(grade4)
                elif 'test score of at least Band' in grade1:
                    grade2 = grade1.split("test score of at least Band")
                    grade3 = grade2[1].split('.')
                    grade4 = grade3[0].strip()
                    print(grade4)
                    prere1grades.append(grade4)
        if len(titles) != len(prere1grades):
            prere1grades.append('')

        #get level codes
        if "Master" in title:
            code = "MST"
        elif "Graduate Certificate" in title:
            code = "GCERT"
        elif "Graduate Diploma":
            code = 'GDIP'
        else:
            code = ''
        print(code)
        level_codes.append(code)

        # get faculty
        meta = soup.find_all('meta')
        for tag in meta:
            text = str(tag)
            if 'ResponsibleFaculty' in text:
                facutly = tag.get('content')
                if 'College of' in facutly:
                    print(facutly)
                    faculties.append(facutly)
                    break

        if len(titles) != len(faculties):
            faculties.append('')

        # set university name
        uni_name = 'University of Tasmania'
        uni_names.append(uni_name)

        # get local fees
        local_fees.append('')

        # set currency
        currencies.append('AUD')

        # set currency_time
        currency_times.append('Year')

        # set duration time
        if dur_3 is not None:
            if float(dur_3) == 1.0:
                duration_times.append('Year')
            elif float(dur_3) > 1:
                duration_times.append('Years')

        if len(duration_times) != len(titles):
            duration_times.append('Year')

        # set fulltime
        full_times.append('Yes')

        # set parttime
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

        # remarks
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
        print('skipped urls are: ' + str(skipped))
        print('duration: ' + str(durations))
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
    'Remarks': remarks
})

test_df.to_csv(r'/Users/zeinalabidin/desktop/CSV_files/TasmeniaUniversityPostgradCourses101-155.csv', index=False, header=True)

for x in skipped:
    print('(skipped) ' +x)
