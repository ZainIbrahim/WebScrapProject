from requests import get
from bs4 import BeautifulSoup
import time
import pandas as pd

uni_names, country_names, titles, level_codes, descriptions, faculties, int_fees, currencies, cities, local_fees, skipped = (
[] for i in range(11))
currency_times, durations, duration_times, full_times, part_times, prere1s, prere2s, prere3s, prere1grades, prere2grades, prere3grades = (
[] for i in range(11))
linksss, course_langs, availabilities, career_outcomes, onlines, offlines, distances, face_to_faces, blendeds, remarks = (
[] for i in range(10))
subject_or_unit_name_1, subject_or_unit_name_2, subject_or_unit_name_3, subject_or_unit_name_4, subject_or_unit_name_5, subject_or_unit_name_6, subject_or_unit_name_7, subject_or_unit_name_8, subject_or_unit_name_9, subject_or_unit_name_10 = (
[] for i in range(10))
subject_or_unit_desc_1, subject_or_unit_desc_2, subject_or_unit_desc_3, subject_or_unit_desc_4, subject_or_unit_desc_5, subject_or_unit_desc_6, subject_or_unit_desc_7, subject_or_unit_desc_8, subject_or_unit_desc_9, subject_or_unit_desc_10 = (
[] for i in range(10))
subject_or_unit_object_1, subject_or_unit_object_2, subject_or_unit_object_3, subject_or_unit_object_4, subject_or_unit_object_5, subject_or_unit_object_6, subject_or_unit_object_7, subject_or_unit_object_8, subject_or_unit_object_9, subject_or_unit_object_10 = (
[] for i in range(10))

'''Collect data'''
with open('links.txt') as f:
    for line in f:

        # url = 'https://www.utas.edu.au/courses/s4a'
        url = line.replace('\n', '')
        request = get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(request.text, 'html.parser')
        # print(soup.prettify())

        # get title
        if soup.find(class_='l-object-page-header--page-title'):
            title = soup.find(class_='l-object-page-header--page-title').text
            print(title)
            titles.append(title)
        else:
            skipped.append(url)
            continue

        # get duration
        '''
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
        '''
        durations.append('')

        '''
        #get location
        duration_and_location = soup.find(class_='g-row g-row__pad-sm')
        for div in duration_and_location.find_all(class_='g-col g-col-global-1-1 g-col-sm-1-1 g-col-md-1-3'):
            if 'Location' in div.h3.text:
                h3_tag = div.h3
                if h3_tag.find_next('dt'):
                    campus = h3_tag.find_next('dt').text
                    print(campus)
                    cities.append(campus)
        print('The number of citiyes are : '+str(cities))
        if len(titles) != len(cities):
            cities.append('Hobart')
        '''
        cities.append('')

        # get international fees
        p_tag = soup.find_all('p')
        for p in p_tag:
            if "Total Course Fee (international students)" in p.text:
                fees = p.text
                fee1 = p.text.split('$')
                fee2 = fee1[1].split('AUD')
                fee3 = fee2[0].strip()
                print(fee3)
                int_fees.append(fee3)

        if len(titles) != len(int_fees):
            int_fees.append('')

        # get description
        h4_tag = soup.find_all('h4')
        for h4 in h4_tag:
            if 'Course objectives' in h4.text:
                if h4.find_next(class_='richtext richtext__medium'):
                    desc = h4.find_next(class_='richtext richtext__medium')
                    if desc.p:
                        desc1 = desc.p.text
                        print(desc1)
                        descriptions.append(desc1)

        if len(titles) != len(descriptions):
            if len(soup.find_all(class_='lede')) > 1:
                div = soup.find_all(class_='lede')[1].text
                print(div)
                descriptions.append(div)

        if len(titles) != len(descriptions):
            descriptions.append('')

        # get career outcomes
        h2_tag = soup.find_all('h2')
        for h2 in h2_tag:
            if 'Career outcomes' in h2.text:
                if h2.find_next('p'):
                    career = h2.find_next('p').text
                    print(career)
                    career_outcomes.append(career)

        if len(titles) != len(career_outcomes):
            career_outcomes.append('')

        # get prerequisite 1
        requisite1 = soup.find_all('p')
        for p in requisite1:
            if 'Applicants are ranked by ATAR' in p.text:
                print('ATAR')
                prere1s.append('ATAR')

        if len(titles) != len(prere1s):
            prere1s.append('')

        # get prerequisite 1 grade
        for p in requisite1:
            if 'receive an offer for this course in 2021 will be' in p.text:
                grade1 = p.text
                grade2 = grade1.split("receive an offer for this course in 2021 will be")
                grade3 = grade2[1].replace('.', '')
                grade4 = grade3.strip()
                print(grade4)
                prere1grades.append(grade4)

        if len(titles) != len(prere1grades):
            prere1grades.append('')

        # get level codes
        if "Diploma" in title:
            code = "DIP"
        elif "Bachelor" in title:
            code = "BA"
        elif "Associate Degree":
            code = 'ADEG'
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
        '''
        if dur_3 is not None:
            if float(dur_3) == 1.0:
                duration_times.append('Year')
            elif float(dur_3) > 1:
                duration_times.append('Years')

        if len(duration_times) != len(titles):
            duration_times.append('Year')
        '''
        duration_times.append('')
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

        '''=================Subject/unit names, subject/unit descripitons, subject/unit objectives======================='''
        # get subject or unit names
        subjects_or_units = set()


        h2_tagz = soup.find('h2',id='course-structure')

        name = h2_tagz.find_next(class_='accordion js-accordion-container')
        name2 = name.find(class_='accordion--content course-structure')
        #print('I am working: '+str(name2))
        if name2:
            linkz = name2.find_all('a')
            for link in linkz:
                if 'https://www.utas.edu.au/courses/' in link.get('href'):
                    aaa = link.get('href')
                    #print('this is the number of links: '+aaa)
                    subjects_or_units.add(aaa)
        

        h2_tagz = soup.find('h2',id='course-structure')
        div_tagz = h2_tagz.find_next(class_='accordion js-accordion-container')
        div_tagz2 = div_tagz.find(class_='accordion--content course-structure')
        if div_tagz2:
            linkz = div_tagz.find_all('a')
            for link in linkz:
                if 'https://www.utas.edu.au/courses/university-college/units/' in link.get('href'):
                    aaa = link.get('href')
                    #print('this is the number of links: '+aaa)
                    subjects_or_units.add(aaa)

        #add  third way of getting links
        h2_tagz = soup.find('h2', id='course-structure')
        div_tagz = h2_tagz.find_next(class_='accordion js-accordion-container')
        div_tagz2 = div_tagz.find(class_='accordion--panel js-accordion-panel')
        if div_tagz2:
            linkz = div_tagz2.find_all('a')
            for link in linkz:
                if 'https://www.utas.edu.au/courses/cse/units/' in link.get('href'):
                    aaa = link.get('href')
                    subjects_or_units.add(aaa)


        print("========="+str(subjects_or_units))
        if len(subjects_or_units) == 0:
            #print('i not working')
            subject_or_unit_name_1.append('')
            subject_or_unit_desc_1.append('')
            subject_or_unit_object_1.append('')

        subject_names = []
        subject_descriptions = []
        subject_objectives = []
        for x in subjects_or_units:
            # url2 = 'https://www.utas.edu.au/courses/cse/units/kla100-food-and-fibre-production-in-a-global-market'
            request2 = get(x, headers={'User-Agent': 'Mozilla/5.0'})
            soup2 = BeautifulSoup(request2.text, 'html.parser')
            # print(soup2)

            # get subject titles
            subject_name_renew = []
            if soup2.find('header', id='title'):
                subj_title = soup2.find('header', id='title').h1.text
                print(subj_title)
                subject_name_renew.append(subj_title)

            # get subject descripiton
            subject_description_renew = []
            if soup2.find('div', class_='unit-intro'):
                try:
                    subj_desc = soup2.find('div', class_='unit-intro').p.text
                    print(subj_desc)
                    subject_description_renew.append(subj_desc)
                except:
                    subject_description_renew.append('')

            # get subject objectives
            subject_objective_renew = []
            td_tagz = None
            h3_tagz = soup2.find_all('h3')
            for h3 in h3_tagz:
                if 'Learning Outcomes' in h3.text:
                    table_tagz = h3.find_next('table')
                    for tr in table_tagz.find_all('tr'):
                        if len(tr.find_all('td')) > 1:
                            td_tagz = tr.find_all('td')[1].text
                            print(td_tagz)
                            subject_objective_renew.append(td_tagz)

            subject_names.append(', '.join(subject_name_renew))
            subject_descriptions.append(', '.join(subject_description_renew))
            subject_objectives.append(', '.join(subject_objective_renew))

        # loading data
        try:
            subject_or_unit_name_1.append(subject_names[0])
            subject_or_unit_name_2.append(subject_names[1])
            subject_or_unit_name_3.append(subject_names[2])
            subject_or_unit_name_4.append(subject_names[3])
            subject_or_unit_name_5.append(subject_names[4])
            subject_or_unit_name_6.append(subject_names[5])
            subject_or_unit_name_7.append(subject_names[6])
            subject_or_unit_name_8.append(subject_names[7])
            subject_or_unit_name_9.append(subject_names[8])
            subject_or_unit_name_10.append(subject_names[9])

        except:
            pass

        # adding null values
        if len(subject_or_unit_name_2) != len(subject_or_unit_name_1):
            subject_or_unit_name_2.append('')
        if len(subject_or_unit_name_3) != len(subject_or_unit_name_1):
            subject_or_unit_name_3.append('')
        if len(subject_or_unit_name_4) != len(subject_or_unit_name_1):
            subject_or_unit_name_4.append('')
        if len(subject_or_unit_name_5) != len(subject_or_unit_name_1):
            subject_or_unit_name_5.append('')
        if len(subject_or_unit_name_6) != len(subject_or_unit_name_1):
            subject_or_unit_name_6.append('')
        if len(subject_or_unit_name_7) != len(subject_or_unit_name_1):
            subject_or_unit_name_7.append('')
        if len(subject_or_unit_name_8) != len(subject_or_unit_name_1):
            subject_or_unit_name_8.append('')
        if len(subject_or_unit_name_9) != len(subject_or_unit_name_1):
            subject_or_unit_name_9.append('')
        if len(subject_or_unit_name_10) != len(subject_or_unit_name_1):
            subject_or_unit_name_10.append('')

        try:
            subject_or_unit_desc_1.append(subject_descriptions[0])
            subject_or_unit_desc_2.append(subject_descriptions[1])
            subject_or_unit_desc_3.append(subject_descriptions[2])
            subject_or_unit_desc_4.append(subject_descriptions[3])
            subject_or_unit_desc_5.append(subject_descriptions[4])
            subject_or_unit_desc_6.append(subject_descriptions[5])
            subject_or_unit_desc_7.append(subject_descriptions[6])
            subject_or_unit_desc_8.append(subject_descriptions[7])
            subject_or_unit_desc_9.append(subject_descriptions[8])
            subject_or_unit_desc_10.append(subject_descriptions[9])
        except:
            pass

        # adding null values
        if len(subject_or_unit_desc_2) != len(subject_or_unit_desc_1):
            subject_or_unit_desc_2.append('')
        if len(subject_or_unit_desc_3) != len(subject_or_unit_desc_1):
            subject_or_unit_desc_3.append('')
        if len(subject_or_unit_desc_4) != len(subject_or_unit_desc_1):
            subject_or_unit_desc_4.append('')
        if len(subject_or_unit_desc_5) != len(subject_or_unit_desc_1):
            subject_or_unit_desc_5.append('')
        if len(subject_or_unit_desc_6) != len(subject_or_unit_desc_1):
            subject_or_unit_desc_6.append('')
        if len(subject_or_unit_desc_7) != len(subject_or_unit_desc_1):
            subject_or_unit_desc_7.append('')
        if len(subject_or_unit_desc_8) != len(subject_or_unit_desc_1):
            subject_or_unit_desc_8.append('')
        if len(subject_or_unit_desc_9) != len(subject_or_unit_desc_1):
            subject_or_unit_desc_9.append('')
        if len(subject_or_unit_desc_10) != len(subject_or_unit_desc_1):
            subject_or_unit_desc_10.append('')

        try:
            subject_or_unit_object_1.append(subject_objectives[0])
            subject_or_unit_object_2.append(subject_objectives[1])
            subject_or_unit_object_3.append(subject_objectives[2])
            subject_or_unit_object_4.append(subject_objectives[3])
            subject_or_unit_object_5.append(subject_objectives[4])
            subject_or_unit_object_6.append(subject_objectives[5])
            subject_or_unit_object_7.append(subject_objectives[6])
            subject_or_unit_object_8.append(subject_objectives[7])
            subject_or_unit_object_9.append(subject_objectives[8])
            subject_or_unit_object_10.append(subject_objectives[9])
        except:
            pass

        #adding null values
        if len(subject_or_unit_object_2) != len(subject_or_unit_object_1):
            subject_or_unit_object_2.append('')
        if len(subject_or_unit_object_3) != len(subject_or_unit_object_1):
            subject_or_unit_object_3.append('')
        if len(subject_or_unit_object_4) != len(subject_or_unit_object_1):
            subject_or_unit_object_4.append('')
        if len(subject_or_unit_object_5) != len(subject_or_unit_object_1):
            subject_or_unit_object_5.append('')
        if len(subject_or_unit_object_6) != len(subject_or_unit_object_1):
            subject_or_unit_object_6.append('')
        if len(subject_or_unit_object_7) != len(subject_or_unit_object_1):
            subject_or_unit_object_7.append('')
        if len(subject_or_unit_object_8) != len(subject_or_unit_object_1):
            subject_or_unit_object_8.append('')
        if len(subject_or_unit_object_9) != len(subject_or_unit_object_1):
            subject_or_unit_object_9.append('')
        if len(subject_or_unit_object_10) != len(subject_or_unit_object_1):
            subject_or_unit_object_10.append('')



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
        print('city: ' + str(cities))
        print('subject name: ' + str(len(subject_or_unit_name_1)))
        print('subject name: ' + str(len(subject_or_unit_name_2)))
        print('subject name: ' + str(len(subject_or_unit_name_3)))
        print('subject name: ' + str(len(subject_or_unit_name_4)))
        print('subject name: ' + str(len(subject_or_unit_name_5)))
        print('subject name: ' + str(len(subject_or_unit_name_6)))
        print('subject name: ' + str(len(subject_or_unit_name_7)))
        print('subject name: ' + str(len(subject_or_unit_name_8)))
        print('subject name: ' + str(len(subject_or_unit_name_9)))
        print('subject name: ' + str(len(subject_or_unit_name_10)))

        print('subject description: ' + str(len(subject_or_unit_desc_1)))
        print('subject description: ' + str(len(subject_or_unit_desc_2)))
        print('subject description: ' + str(len(subject_or_unit_desc_3)))
        print('subject description: ' + str(len(subject_or_unit_desc_4)))
        print('subject description: ' + str(len(subject_or_unit_desc_5)))
        print('subject description: ' + str(len(subject_or_unit_desc_6)))
        print('subject description: ' + str(len(subject_or_unit_desc_7)))
        print('subject description: ' + str(len(subject_or_unit_desc_8)))
        print('subject description: ' + str(len(subject_or_unit_desc_9)))
        print('subject description: ' + str(len(subject_or_unit_desc_10)))

        print('subject objective: ' + str(len(subject_or_unit_object_1)))
        print('subject objective: ' + str(len(subject_or_unit_object_2)))
        print('subject objective: ' + str(len(subject_or_unit_object_3)))
        print('subject objective: ' + str(len(subject_or_unit_object_4)))
        print('subject objective: ' + str(len(subject_or_unit_object_5)))
        print('subject objective: ' + str(len(subject_or_unit_object_6)))
        print('subject objective: ' + str(len(subject_or_unit_object_7)))
        print('subject objective: ' + str(len(subject_or_unit_object_8)))
        print('subject objective: ' + str(len(subject_or_unit_object_9)))
        print('subject objective: ' + str(len(subject_or_unit_object_10)))

        print(
            '====================================================================================================================')
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
    'Subject or unit name 1': subject_or_unit_name_1,
    'Subject or unit name 2': subject_or_unit_name_2,
    'Subject or unit name 3': subject_or_unit_name_3,
    'Subject or unit name 4': subject_or_unit_name_4,
    'Subject or unit name 5': subject_or_unit_name_5,
    'Subject or unit name 6': subject_or_unit_name_6,
    'Subject or unit name 7': subject_or_unit_name_7,
    'Subject or unit name 8': subject_or_unit_name_8,
    'Subject or unit name 9': subject_or_unit_name_9,
    'Subject or unit name 10': subject_or_unit_name_10,
    'subject or unit description 1': subject_or_unit_desc_1,
    'subject or unit description 2': subject_or_unit_desc_2,
    'subject or unit description 3': subject_or_unit_desc_3,
    'subject or unit description 4': subject_or_unit_desc_4,
    'subject or unit description 5': subject_or_unit_desc_5,
    'subject or unit description 6': subject_or_unit_desc_6,
    'subject or unit description 7': subject_or_unit_desc_7,
    'subject or unit description 8': subject_or_unit_desc_8,
    'subject or unit description 9': subject_or_unit_desc_9,
    'subject or unit description 10': subject_or_unit_desc_10,
    'Subect or unit objective 1': subject_or_unit_object_1,
    'Subect or unit objective 2': subject_or_unit_object_2,
    'Subect or unit objective 3': subject_or_unit_object_3,
    'Subect or unit objective 4': subject_or_unit_object_4,
    'Subect or unit objective 5': subject_or_unit_object_5,
    'Subect or unit objective 6': subject_or_unit_object_6,
    'Subect or unit objective 7': subject_or_unit_object_7,
    'Subect or unit objective 8': subject_or_unit_object_8,
    'Subect or unit objective 9': subject_or_unit_object_9,
    'Subect or unit objective 10': subject_or_unit_object_10
})

test_df.to_csv(r'/Users/zeinalabidin/desktop/CSV_files/TasmeniaUniversity11-20.csv', index=False, header=True)

for x in skipped:
    print('(skipped) ' + x)

