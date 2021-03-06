from requests import get
from bs4 import BeautifulSoup
import pandas as pd

'''collect international student fees'''
url_int_fees = 'https://www.kbs.edu.au/admissions/fees/international-fees'
request_int_fees = get(url_int_fees)
soup_int_fees = BeautifulSoup(request_int_fees.text, 'html.parser')
#print(soup_int_fees.prettify())
table_tag = soup_int_fees.find('table')
t_body = table_tag.find('tbody')
int_fee_course = {}
for tr in t_body.find_all('tr'):
    td_tit = tr.find_all('td')[0].text.strip()
    td_price = tr.find_all('td')[3].text.strip()
    int_fee_course[td_tit] = td_price
#print(fee_course)

'''collect local student fees'''
url_loc_fees = 'https://www.kbs.edu.au/admissions/fees/domestic-fees'
request_loc_fees = get(url_loc_fees)
soup_loc_fees = BeautifulSoup(request_loc_fees.text, 'html.parser')
#print(soup_loc_fees.prettify())
table_tag = soup_loc_fees.find('table')
t_body = table_tag.find('tbody')
loc_fee_course = {}
for tr in t_body.find_all('tr'):
    td_tit = tr.find_all('td')[0].text.strip()
    td_price = tr.find_all('td')[3].text.strip()
    loc_fee_course[td_tit] = td_price
#print(loc_fee_course)

'''Collect links'''
#collect the first set of links
url = 'https://www.kbs.edu.au/courses'
request = get(url)
soup = BeautifulSoup(request.text, 'html.parser')
#print(soup.prettify())

links = []
div_tag = soup.find_all(class_='view-content')[1]
for div_tag_ in div_tag.find_all(class_='views-row'):
    a_tag = div_tag_.a.get('href')
    #print(a_tag)
    links.append(a_tag)

'''collect data'''
uni_names, titles , level_codes , descriptions , durations, locations, country_names , faculties, int_fees, linksss =([] for i in range(10))
loc_fees, currencies, currency_times, duration_times, glob_ifs, wr_ranges, mode_of_studies, prere1s, prere2s, prere3s, career_outcomes, remarks =([] for j in range(12))
prere1grades,prere2grades, prere3grades, course_langs, availabilities, abbreviations, course_delivery_modes, full_times, part_times, blendeds, onlines, offlines, free_tafes, face_to_faces, distances=([] for j in range(15))
subject_or_unit_name_1, subject_or_unit_name_2, subject_or_unit_name_3, subject_or_unit_name_4, subject_or_unit_name_5, subject_or_unit_name_6,subject_or_unit_name_7, subject_or_unit_name_8, subject_or_unit_name_9, subject_or_unit_name_10  =([] for i in range(10))
subject_or_unit_desc_1, subject_or_unit_desc_2, subject_or_unit_desc_3, subject_or_unit_desc_4, subject_or_unit_desc_5, subject_or_unit_desc_6, subject_or_unit_desc_7, subject_or_unit_desc_8, subject_or_unit_desc_9,subject_or_unit_desc_10 =([] for i in range(10))
subject_or_unit_object_1, subject_or_unit_object_2, subject_or_unit_object_3, subject_or_unit_object_4, subject_or_unit_object_5, subject_or_unit_object_6, subject_or_unit_object_7, subject_or_unit_object_8, subject_or_unit_object_9, subject_or_unit_object_10 =([] for i in range(10))

for x in range(len(links)):
    url2 = 'https://www.kbs.edu.au'+links[x]
    request2 = get(url2)
    soup2 = BeautifulSoup(request2.text, 'html.parser')
    #print(soup2.prettify())

    location_tag = soup2.find_all('h6')
    for a in location_tag:
        if "Locations" in a.text:
            location = a.find_next('p').text
            #print(location)
            ll = location.split('/')
            for i in range(len(ll)):
                if "Online" not in ll[i]:
                    locations2 = ll[i]
                    #print(locations2)
                    ####################################################################################

                    #set university name
                    uni_name = 'Kaplan Business School'
                    #print(uni_name)
                    uni_names.append(uni_name)

                    #set country
                    country = 'Australia'
                    #print(country)
                    country_names.append(country)

                    #get title
                    title_tag = soup2.find(class_='course__field-name')
                    title = title_tag.h2.text
                    #print(title)
                    titles.append(title)

                    #set course level code
                    if title.startswith('Master') or title.startswith('MBA'):
                        level_code = 'MST'
                        #print(level_code)
                        level_codes.append(level_code)
                    elif title.startswith('Graduate Diploma'):
                        level_code = 'GDIP'
                        #print(level_code)
                        level_codes.append(level_code)
                    elif title.startswith('Graduate Certificate'):
                        level_code = 'GCERT'
                        #print(level_code)
                        level_codes.append(level_code)
                    elif title.startswith('Bachelor'):
                        level_code = 'BA'
                        #print(level_code)
                        level_codes.append(level_code)
                    elif title.startswith('Diploma'):
                        level_code = 'DIP'
                        #print(level_code)
                        level_codes.append(level_code)
                    else:
                        level_code = 'PATHWAY'
                        #print(level_code)
                        level_codes.append(level_code)

                    #set faculty
                    if "Accounting" or "Business" or "Qualifying" in title.text:
                        faculty = 'Business & Commerce & Finance & Accounting'
                        #print(faculty)
                        faculties.append(faculty)

                    #get international student fees
                    for key in int_fee_course:
                        #print(int_fee_course[key])
                        #print(key)
                        if 'MBA' in title:
                            tt = title.split('Master')
                            tts = tt[1]
                            ttss = 'Master'+tts
                            #print(ttss)
                            if ttss == key:
                                international_fee = int_fee_course[key]
                                #print(international_fee)
                                int_fees.append(international_fee)
                     #   elif 'and' in key:
                      #      int_fees.append('NULL')

                        elif title == key:
                            international_fee = int_fee_course[key]
                            #print(international_fee)
                            int_fees.append(international_fee)
                    if len(titles) != len(int_fees):
                        int_fees.append('')
                    # get local student fees
                    for key in loc_fee_course:
                        #print(loc_fee_course[key])
                        #print(key)
                        if 'MBA' in title:
                            tt = title.split('Master')
                            tts = tt[1]
                            ttss = 'Master'+tts
                            #print(ttss)
                            if ttss == key:
                                local_fee = loc_fee_course[key]
                                #print(local_fee)
                                loc_fees.append(local_fee)
                    if len(titles) != len(loc_fees):
                        loc_fees.append('')
                        '''
                        if 'BACHELOR OF BUSINESS (HOSPITALITY & TOURISM MANAGEMENT)' in title:
                            #kkk = title.replace("BACHELOR OF BUSINESS (HOSPITALITY & TOURISM MANAGEMENT)", "BACHELOR OF BUSINESS (HOSPITALITY and TOURISM MANAGEMENT)")
                            #print(kkk)
                            if 'BACHELOR OF BUSINESS (HOSPITALITY and TOURISM MANAGEMENT)' in key:
                                local_fee = loc_fee_course[key]
                                print(local_fee)
                                loc_fees.append(local_fee)
                         #   loc_fees.append('NULL')
                         '''

                        if title == key:
                            local_fee = loc_fee_course[key]
                            #print(local_fee)
                            loc_fees.append(local_fee)
                    #set currency
                    currency = 'AUD'
                    currencies.append(currency)

                    #set currency_time
                    currency_time = 'Year'
                    currency_times.append(currency_time)

                    #get course durations
                    duration = soup2.find(class_='course__field-typical-duration course--field').h4.text.strip()
                    #print(duration)
                    durations.append(duration)

                    #set duration time
                    duration_time = 'Years'
                    duration_times.append(duration_time)

                    #prerequiste 1
                    prere1 = ''
                    prere1s.append(prere1)
                    #prerequistie 1 grade
                    prere1grade = ''
                    prere1grades.append(prere1grade)
                    #prerequisite 2
                    prere2 = ''
                    prere2s.append(prere2)
                    #prerequisite 2 grade
                    prere2grade = ''
                    prere2grades.append(prere2grade)
                    #prerequisite 3
                    prere3 = ''
                    prere3s.append(prere3)
                    #prerequisite 3 grade
                    prere3grade = ''
                    prere3grades.append(prere3grade)

                    #get website
                        #get it from the list: links
                    linksss.append(url2)

                    #set course language
                    course_lang = 'English'
                    course_langs.append(course_lang)

                    #get availability
                    availability = 'A'
                    availabilities.append(availability)

                    #get course description
                    description_tag = soup2.find(class_='field__content col col-md-8')
                    description = description_tag.p.text.strip()
                    #print(description)
                    descriptions.append(description)


                    # set abbreviations
                    abbreviation = ('AU','KBS', 'PA', 'ACCOUNT', 'PRO', 'PG', 'MDP', 'MP', 'POSTGRAD',
                                     'POSTGRADUATE', 'MASTERS', 'FEBRUARY-SUMMER', 'JULY-WINTER','FEB',
                                     'SUMMER','JULY', 'WINTER'
                                     )
                    abbreviations.append(abbreviation)



                    #career outcomes
                    career_renew= []
                    if soup2.find(class_='course__field-career-outcomes course--field'):
                        career = soup2.find(class_='course__field-career-outcomes course--field')
                        for a in career.find_all('field__item'):
                            career_ = a.text
                            career_renew.append(career_)
                        career_outcomes.append(', '.join(career_renew))

                    if len(titles) != len(career_outcomes):
                        career_outcomes.append('')




                    #free tafe
                    free_tafes.append('No')

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

                    #full time
                    full_times.append('Yes')

                    #part time
                    part_times.append('')

                    #remarks
                    remarks.append('')

                    #course delivery modes
                    course_delivery_modes.append('Normal')
                    ####################################################################################
                    locations.append(locations2)



                    '''scrape subject or unit name, description and objective'''
                    subject_link = []

                    subject_name = []
                    subject_description = []
                    h6_tagz = soup2.find_all('h6')
                    for h6 in h6_tagz:
                        subject_name_renew = []
                        subject_description_renew = []
                        if 'Course subjects' in h6.text:
                            div_tagz = h6.find_next(class_='paragraph paragraph--type--accordion-content paragraph--view-mode--default')
                            div_tagz_ = div_tagz.find(class_='panel panel-default')
                            table_tagz = div_tagz_.find('table', class_='table table-borderless')
                            t_bodyz = table_tagz.find('tbody')
                            a_tagz = t_bodyz.find_all('a')
                            for a in a_tagz:
                                link_to_subject = a.get('href')
                                print(link_to_subject)
                                subject_link.append(link_to_subject)

                    ''' go to the links to scrape the name and description of courses'''
                    for x in range(len(subject_link)):

                        urlz = 'https://www.kbs.edu.au'+ subject_link[x]
                        requestz = get(urlz)
                        soupz = BeautifulSoup(requestz.text, 'html.parser')
                        # print(soupz.prettify())
                        span_tag_name = soupz.find('span', class_='popup-header').text
                        print(span_tag_name)
                        subject_name_renew.append(span_tag_name)

                        span_tag_desc = soupz.find('span', class_='popup-description').text
                        print(span_tag_desc)
                        subject_description_renew.append(span_tag_desc)

                        subject_name.append(', '.join(subject_name_renew))
                        subject_description.append(', '.join(subject_description_renew))

                        print(subject_name)
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


    if len(titles) != len(locations):
        locations.append('Sydney')
    print('---------------------------------------------------------------------------------------------------')

'''
print('title'+ str(len(titles)))
print('description'+ str(len(descriptions)))
print('duration'+ str(len(durations)))
print('Locations'+ str(len(locations)))
print('links'+ str(len(linksss)) )
print('int'+ str(len(int_fees)) )
print('loc'+ str(len(loc_fees)) )
print('location'+ str(len(locations)) )
print(''+ str(len(level_codes)) )
print(''+ str(len(uni_names)) )
print(''+ str(len(faculties)) )
print(''+ str(len(currencies)) )
print(''+ str(len(currency_times)) )
print(''+ str(len(duration_times)) )
print(''+ str(len(prere1s)) )
print(''+ str(len(linksss)) )
'''

#print( loc_fees)

test_df = pd.DataFrame({
    'Level code': level_codes,
    'University': uni_names,
    'City': locations,
    'Courses': titles,
    'Faculty': faculties,
    'Int fees': int_fees,
    'Local fees': loc_fees,
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
    'abbreviation': abbreviations,
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
})


test_df.to_csv(r'/Users/zeinalabidin/desktop/CSV_files/KaplanBusinessSchool.csv', index = False, header=True)

# course title
# course overview
# course location
# course length


#level code (done)
#university (static)(done)
#city (done)
#country (static) (done)
#course (I already have) (done)
#faculty (static) (done)
#int_fees (done)
#loc_fees (done)
#currency (static)
#currency_Time (static)
#Duration
#Duration_Time (static)
#Glob_if
#Mode of study
#prerequisite 1
#prerequisite_1_grade
#prerequisite 2
#prerequisite_2_grade
...
#prerequisite 5
#prerequisite_5_grade
#prerequisite_1_certificate
#prerequisite_2_certificate
#prerequisite_3_certificate

#website (easy, peasy)
#course_language (static)
#availability
#part_full
#study_mode
#description (I already have)
#inst_id
#abbreviation


