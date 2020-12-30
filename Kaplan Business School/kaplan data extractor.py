from requests import get
from bs4 import BeautifulSoup
import time
import pandas as pd
import datetime

start = time.time()

uni_names, country_names, titles, level_codes, descriptions, faculties, int_fees, currencies, cities, local_fees, skipped =([] for i in range(11))
currency_times, durations, duration_times, full_times, part_times, prere1s, prere2s, prere3s, prere1grades,prere2grades,prere3grades = ([] for i in range(11))
linksss, course_langs, availabilities,career_outcomes, onlines, offlines, distances, face_to_faces, blendeds, remarks = ([] for i in range(10))
subject_or_unit_name_1, subject_or_unit_name_2, subject_or_unit_name_3, subject_or_unit_name_4, subject_or_unit_name_5, subject_or_unit_name_6,subject_or_unit_name_7, subject_or_unit_name_8, subject_or_unit_name_9, subject_or_unit_name_10  =([] for i in range(10))
subject_or_unit_desc_1, subject_or_unit_desc_2, subject_or_unit_desc_3, subject_or_unit_desc_4, subject_or_unit_desc_5, subject_or_unit_desc_6, subject_or_unit_desc_7, subject_or_unit_desc_8, subject_or_unit_desc_9,subject_or_unit_desc_10 =([] for i in range(10))
subject_or_unit_object_1, subject_or_unit_object_2, subject_or_unit_object_3, subject_or_unit_object_4, subject_or_unit_object_5, subject_or_unit_object_6, subject_or_unit_object_7, subject_or_unit_object_8, subject_or_unit_object_9, subject_or_unit_object_10 =([] for i in range(10))

'''Collect data'''
with open('links.txt') as f:
    for line in f:
        url = 'https://www.kbs.edu.au'+line.replace('\n','')
        request = get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(request.text, 'html.parser')
        #print(soup.prettify())


        #get title
        title_tag = soup.find(class_='course__field-name').text.strip()
        print(title_tag)
        titles.append(title_tag)

        #get duration
        duration_tag = soup.find(class_='course__field-typical-duration course--field')
        if duration_tag:
            strong_tag = duration_tag.find('strong')
            if strong_tag:
                duration = strong_tag.text
                print(duration)
                durations.append(duration)

        if len(durations) != len(titles):
            durations.append(durations)

        #get city
        location_tag = soup.find_all('h6')
        for location in location_tag:
            if 'Locations' in location.text or 'Location' in location.text:
                city = location.find_next('p').text.strip()
                print(city)
                cities.append(city)

        #get international fees
        int_fees.append('')

        #get description
        overview_tab = soup.find(class_='course__overview')
        field_content = overview_tab.find(class_='field__content col col-md-8')
        description = field_content.find('p').text.strip()
        print(description)
        descriptions.append(description)



        #subject names, descriptions
        subject_link = []
        subject_name = []
        subject_description = []
        h6_tagz = soup.find_all('h6')
        for h6 in h6_tagz:
            if 'Course subjects' in h6.text:
                div_tagz = h6.find_next(class_='paragraph paragraph--type--accordion-content paragraph--view-mode--default')
                div_tagz_ = div_tagz.find(class_='panel panel-default')
                table_tagz = div_tagz_.find('table', class_='table table-borderless')
                t_bodyz = table_tagz.find('tbody')
                a_tagz = t_bodyz.find_all('a')
                for a in a_tagz:
                    link_to_subject = a.get('href')
                    #print(link_to_subject)
                    subject_link.append(link_to_subject)
        #print(subject_link)

        ''' go to the links to scrape the name and description of courses'''
        for x in range(len(subject_link)):
            urlz = 'https://www.kbs.edu.au' + subject_link[x]
            requestz = get(urlz)
            soupz = BeautifulSoup(requestz.text, 'html.parser')
            # print(soupz.prettify())

            #get subject name
            subject_name_renew = []
            span_tag_name = soupz.find('span', class_='popup-header').text
            print(span_tag_name)
            subject_name_renew.append(span_tag_name)

            #get subject description
            subject_description_renew = []
            span_tag_desc = soupz.find('span', class_='popup-description').text
            print(span_tag_desc)
            subject_description_renew.append(span_tag_desc)

            subject_name.append(', '.join(subject_name_renew))
            subject_description.append(', '.join(subject_description_renew))

            #print('This this the final list of subject names: ' +str(subject_name))
            #print('This this the final list of subject Descriptions: ' +str(subject_description))


        '''load subject data into variables'''
        try:
            subject_or_unit_name_1.append(subject_name[0])
            subject_or_unit_name_2.append(subject_name[1])
            subject_or_unit_name_3.append(subject_name[2])
            subject_or_unit_name_4.append(subject_name[3])
            subject_or_unit_name_5.append(subject_name[4])
            subject_or_unit_name_6.append(subject_name[5])
            subject_or_unit_name_7.append(subject_name[6])
            subject_or_unit_name_8.append(subject_name[7])
            subject_or_unit_name_9.append(subject_name[8])
            subject_or_unit_name_10.append(subject_name[9])
        except:
            pass

        '''adding none values'''
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
            subject_or_unit_desc_1.append(subject_description[0])
            subject_or_unit_desc_2.append(subject_description[1])
            subject_or_unit_desc_3.append(subject_description[2])
            subject_or_unit_desc_4.append(subject_description[3])
            subject_or_unit_desc_5.append(subject_description[4])
            subject_or_unit_desc_6.append(subject_description[5])
            subject_or_unit_desc_7.append(subject_description[6])
            subject_or_unit_desc_8.append(subject_description[7])
            subject_or_unit_desc_9.append(subject_description[8])
            subject_or_unit_desc_10.append(subject_description[9])
        except:
            pass

        if len(subject_or_unit_desc_5) != len(subject_or_unit_name_1):
            subject_or_unit_desc_5.append('')
        if len(subject_or_unit_desc_6) != len(subject_or_unit_name_1):
            subject_or_unit_desc_6.append('')
        if len(subject_or_unit_desc_7) != len(subject_or_unit_name_1):
            subject_or_unit_desc_7.append('')
        if len(subject_or_unit_desc_8) != len(subject_or_unit_name_1):
            subject_or_unit_desc_8.append('')
        if len(subject_or_unit_desc_9) != len(subject_or_unit_name_1):
            subject_or_unit_desc_9.append('')
        if len(subject_or_unit_desc_10) != len(subject_or_unit_name_1):
            subject_or_unit_desc_10.append('')



        print('-------------------printing the length of lists---------------------')
        print('City: ' + str(len(cities)))
        print('Courses: ' + str(len(titles)))
        print('international fees: ' + str(len(int_fees)))
        print('Duration : ' + str(len(durations)))
        print('Descrtiption : ' + str(len(descriptions)))
        print('subject name: ' + str(len(subject_or_unit_name_1)))
        print('subject description: ' + str(len(subject_or_unit_desc_1)))
        print('subject name 10: ' + str(len(subject_or_unit_name_10)))
        print('subject description 10: ' + str(len(subject_or_unit_desc_10)))

        #time.sleep(1.5)

test_df = pd.DataFrame({
    'City': cities,
    'Courses': titles,
    'Int fees': int_fees,
    'Duration': durations,
    'Descrtiption': descriptions,
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
    'subject or unit description 10': subject_or_unit_desc_10
    })

test_df.to_csv(r'/Users/zeinalabidin/desktop/CSV_files/KaplanCourses11-17.csv', index=False,header=True)
stop = time.time()

print(stop-start)