from requests import get
from bs4 import BeautifulSoup
import time
import pandas as pd

uni_names, country_names, titles, level_codes, descriptions, faculties, int_fees, currencies, cities, local_fees, skipped =([] for i in range(11))
currency_times, durations, duration_times, full_times, part_times, prere1s, prere2s, prere3s, prere1grades,prere2grades,prere3grades = ([] for i in range(11))
linksss, course_langs, availabilities,career_outcomes, onlines, offlines, distances, face_to_faces, blendeds, remarks, course_delivery_modes, free_tafes = ([] for i in range(12))
subject_or_unit_name_1, subject_or_unit_name_2, subject_or_unit_name_3, subject_or_unit_name_4, subject_or_unit_name_5, subject_or_unit_name_6, subject_or_unit_name_7, subject_or_unit_name_8, subject_or_unit_name_9, subject_or_unit_name_10 = ([] for i in range(10))
subject_or_unit_desc_1, subject_or_unit_desc_2, subject_or_unit_desc_3, subject_or_unit_desc_4, subject_or_unit_desc_5, subject_or_unit_desc_6, subject_or_unit_desc_7, subject_or_unit_desc_8, subject_or_unit_desc_9, subject_or_unit_desc_10 = ([] for i in range(10))
subject_or_unit_object_1, subject_or_unit_object_2, subject_or_unit_object_3, subject_or_unit_object_4, subject_or_unit_object_5, subject_or_unit_object_6, subject_or_unit_object_7, subject_or_unit_object_8, subject_or_unit_object_9, subject_or_unit_object_10 = ([] for i in range(10))

'''Collect data'''
with open('links.txt') as f:
    for line in f:

        #url = 'https://www.utas.edu.au/courses/s4a'
        url = 'https://www.tafesa.edu.au'+line.replace('\n','')
        request = get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(request.text, 'html.parser')
        #print(soup.prettify())

        #get title
        if soup.find(class_='cp_title'):
            title = soup.find(class_='cp_title').text
            print(title)
            titles.append(title)
        else:
            skipped.append(url)
            continue

        #get description
        if soup.find(id='CourseDescription'):
            p_tag = soup.find(id='CourseDescription').text.strip()
            print(p_tag)
            descriptions.append(p_tag)

        if len(titles) != len(descriptions):
            descriptions.append('')

        #get duration
        dur4 = None
        if soup.find(class_='cp_table'):
            duration = soup.find(class_='cp_table')
            for cp in duration.find_all(class_='cp_cell'):
                if "month" in cp.text:
                    dur1 = cp.text.split('month')
                    dur2 = dur1[0]
                    if 'Up to' in dur2:
                        dur3 = dur2.split('Up to')
                        dur4 = dur3[1].strip()
                        print(dur4)
                        durations.append(dur4)
                    else:
                        durations.append(dur2)

        if len(titles) != len(durations):
            durations.append('')

        #get city
        h2_tag = soup.find_all('h2')
        for h2 in h2_tag:
            if "Locations & Applications" in h2.text:
                cp_table = h2.find_next(class_='cp_table-wrapper')
                a_tag = cp_table.find('a').text
                print(a_tag)
                cities.append(a_tag)

        if len(titles) != len(cities):
            cities.append('')

        #int fees
        if soup.find(class_='ft_table-row ft_table-fullFee'):
            fee = soup.find(class_='ft_table-row ft_table-fullFee')
            if fee.find(class_='ft_cell col-md-4 col-sm-6 col-xs-8'):
                fee1 = fee.find(class_='ft_cell col-md-4 col-sm-6 col-xs-8').text
                print(fee1)
                int_fees.append(fee1)

        if len(titles) != len(int_fees):
            int_fees.append('')

        #career outcomes
        h3_tag = soup.find_all('h3')
        for h3 in h3_tag:
            if "Employment Outcomes" in h3.text:
                career = h3.find_next('p').text.strip()
                print(career)
                career_outcomes.append(career)

        if len(titles) != len(career_outcomes):
            career_outcomes.append('')

        #get remarks
        h3_tag = soup.find_all('h3')
        for h3 in h3_tag:
            if "Course Admission Requirements" in h3.text:
                remark = h3.find_next('li').text
                print(remark)
                remarks.append(remark)
                break

        if len(titles) != len(remarks):
            remarks.append('')

        #get faculty
        if soup.find('data', id = 'datalayer-contaniner'):
            fac = soup.find('data', id = 'datalayer-contaniner')
            if fac.get('data-industrygroupname'):
                fac1 = fac.get('data-industrygroupname')
                print(fac1)
                faculties.append(fac1)

        if len(titles) != len(faculties):
            faculties.append('')

        #set level codes
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
        else:
            code = ''
        print(code)
        level_codes.append(code)

        # set university name
        uni_name = 'TAFE SA'
        uni_names.append(uni_name)

        # get local fees
        local_fees.append('')

        # set currency
        currencies.append('AUD')

        # set currency_time
        currency_times.append('Year')

        # set duration time
        duration_times.append('Months')



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

        #prerequisite 1
        prere1s.append('')
        #prerequisite 1 grade
        prere1grades.append('')

        #course delivery mode
        if soup.find(class_='col-md-12 cp_content-row study_selector'):
            appren = soup.find(class_='col-md-12 cp_content-row study_selector')
            if appren.find_next(class_='intake_tab-wrapper'):
                trainee = appren.find_next(class_='intake_tab-wrapper')
                a = trainee.find_all_next('a')[1]
                if 'Apprenticeships & Traineeships'in a.text:
                    apprenticeship  = 'Apprenticeships & Traineeships'
                    course_delivery_modes.append(apprenticeship)

        if len(titles) != len(course_delivery_modes):
            course_delivery_modes.append('Normal')

        #free tafe
        free_tafes.append('No')

        '''=================Subject/unit names, subject/unit descripitons, subject/unit objectives======================='''
        # get subject or unit names


        subject_names = []
        subject_descriptions = []
        subject_objectives = []

        # get subject titles
        div_tagz = soup.find(class_='col-md-12 cp_content-row additional_files')
        if div_tagz:
            table_tagz = div_tagz.find_next('table')
            if table_tagz:
                tr_tagz = table_tagz.find_all('tr')[1:]
                for tr in tr_tagz:
                    td_tagz = tr.find('td').text
                    #print(td_tagz)
                    subject_names.append(td_tagz)


        # get subject descripiton
        subject_description_renew = []

        subject_description_renew.append('')

        # get subject objectives
        subject_objective_renew = []

        subject_objective_renew.append('')

        #subject_names.append(subject_name_renew)
        subject_descriptions.append(', '.join(subject_description_renew))
        subject_objectives.append(', '.join(subject_objective_renew))

        if len(subject_descriptions) != len(subject_names):
            subject_names.append('')

        #print('this is the list'+str(subject_names))
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

        # adding null values
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
        print('remarks: ' + str(remarks))
        print('apprenticeship: ' + str(course_delivery_modes))
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
    'Free TAFE': free_tafes,
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

test_df.to_csv(r'/Users/zeinalabidin/desktop/CSV_files/TafeSAInstitueCourses301-428.csv', index=False,
               header=True)

for x in skipped:
    print('(skipped) ' + x)
