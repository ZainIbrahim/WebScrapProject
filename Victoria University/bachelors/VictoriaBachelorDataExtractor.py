from requests import get
from bs4 import BeautifulSoup
import time
import pandas as pd

uni_names, country_names, titles, level_codes, descriptions, faculties, int_fees, currencies, cities, local_fees, skipped =([] for i in range(11))
currency_times, durations, duration_times, full_times, part_times, prere1s, prere2s, prere3s, prere1grades,prere2grades,prere3grades = ([] for i in range(11))
linksss, course_langs, availabilities,career_outcomes, onlines, offlines, distances, face_to_faces, blendeds, remarks = ([] for i in range(10))
subject_or_unit_name_1, subject_or_unit_name_2, subject_or_unit_name_3, subject_or_unit_name_4, subject_or_unit_name_5, subject_or_unit_name_6,subject_or_unit_name_7, subject_or_unit_name_8, subject_or_unit_name_9, subject_or_unit_name_10  =([] for i in range(10))
subject_or_unit_desc_1, subject_or_unit_desc_2, subject_or_unit_desc_3, subject_or_unit_desc_4, subject_or_unit_desc_5, subject_or_unit_desc_6, subject_or_unit_desc_7, subject_or_unit_desc_8, subject_or_unit_desc_9,subject_or_unit_desc_10 =([] for i in range(10))
subject_or_unit_object_1, subject_or_unit_object_2, subject_or_unit_object_3, subject_or_unit_object_4, subject_or_unit_object_5, subject_or_unit_object_6, subject_or_unit_object_7, subject_or_unit_object_8, subject_or_unit_object_9, subject_or_unit_object_10 =([] for i in range(10))

'''Collect data'''
#with open('links.txt') as f:
#    for line in f:

with open('links.txt') as f:
    for line in f:

        #url = 'https://www.utas.edu.au/courses/s4a'
        url = line.replace('\n','')
        request = get(url, headers={'User-Agent': 'Mozilla/5.0'})
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
        if "Diploma" in title:
            code = "DIP"
        elif "Bachelor" in title:
            code = "BA"
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


        '''------------------------------------------subject or unit names, descriptions and objectives -----------------------'''

        #get the first links
        subject_links = []
        div_tagz = soup.find(id='course-structure')
        section_id = div_tagz.find(id='units-and-electives')
        if section_id:
            ul_tagz = section_id.find_all('ul')
            for ul in ul_tagz:
                li_tagz = ul.find_all('li')
                for li in li_tagz:
                    sub_link = li.find('a').get('href')
                    if '/units/' in sub_link:
                        #print(sub_link)
                        #while len(subject_links) <10:
                        subject_links.append(sub_link)
        print ((subject_links))

        #get the name, description and objectives
        subject_name = []
        subject_description = []
        subject_objective = []
        for x in range(len(subject_links)):
            url2 = 'https://www.vu.edu.au'+subject_links[x]
            request2 = get(url2,headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'})
            soup2 = BeautifulSoup(request2.text, 'html.parser')
            #print(soup2.prettify())

            #get subject name
            subject_name_renew = []
            if soup2.find(class_='page-header'):
                h1_tagz = soup2.find(class_='page-header').text.strip()
                print(h1_tagz)
                subject_name_renew.append(h1_tagz)

            #get subject description
            subject_description_renew = []
            if soup2.find(class_='field field-name-body field-type-text-with-summary field-label-hidden'):
                p_tagz = soup2.find(class_='field field-name-body field-type-text-with-summary field-label-hidden').text.strip()
                print(p_tagz)
                subject_description_renew.append(p_tagz)

            #get subject objective
            subject_objective_renew = []
            h2_tagz = soup2.find_all('h2')
            for h2 in h2_tagz:
                if 'Learning Outcomes' in h2.text:
                    table_tagz = h2.find_next('table')
                    tr_tagz = soup.find_all('tr')
                    for tr in tr_tagz:
                        subject_objec = tr.text.strip()
                        print(subject_objec)
                        subject_objective_renew.append(subject_objec)


            subject_name.append(', '.join(subject_name_renew))
            subject_objective.append(', '.join(subject_objective_renew))
            subject_description.append(', '.join(subject_description_renew))

        print('--------------------------------------------------------------------------------------')
        print('--------------------------------------------------------------------------------------')
        print(subject_name)




        print('--------------------------------------------------------------------------------------')
        print('--------------------------------------------------------------------------------------')

        '''load subject data in the variables '''
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

        #adding non values
        if len(subject_or_unit_desc_3) != len(subject_or_unit_name_1):
            subject_or_unit_desc_3.append('')
        if len(subject_or_unit_desc_4) != len(subject_or_unit_name_1):
            subject_or_unit_desc_4.append('')
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


        try:
            subject_or_unit_object_1.append(subject_objective[0])
            subject_or_unit_object_2.append(subject_objective[1])
            subject_or_unit_object_3.append(subject_objective[2])
            subject_or_unit_object_4.append(subject_objective[3])
            subject_or_unit_object_5.append(subject_objective[4])
            subject_or_unit_object_6.append(subject_objective[5])
            subject_or_unit_object_7.append(subject_objective[6])
            subject_or_unit_object_8.append(subject_objective[7])
            subject_or_unit_object_9.append(subject_objective[8])
            subject_or_unit_object_10.append(subject_objective[9])
        except:
            pass

        if len(subject_or_unit_object_3) != len(subject_or_unit_name_1):
            subject_or_unit_object_3.append('')
        if len(subject_or_unit_object_4) != len(subject_or_unit_name_1):
            subject_or_unit_object_4.append('')
        if len(subject_or_unit_object_5) != len(subject_or_unit_name_1):
            subject_or_unit_object_5.append('')
        if len(subject_or_unit_object_6) != len(subject_or_unit_name_1):
            subject_or_unit_object_6.append('')
        if len(subject_or_unit_object_7) != len(subject_or_unit_name_1):
            subject_or_unit_object_7.append('')
        if len(subject_or_unit_object_8) != len(subject_or_unit_name_1):
            subject_or_unit_object_8.append('')
        if len(subject_or_unit_object_9) != len(subject_or_unit_name_1):
            subject_or_unit_object_9.append('')
        if len(subject_or_unit_object_10) != len(subject_or_unit_name_1):
            subject_or_unit_object_10.append('')




        if len(subject_or_unit_desc_1) > len(subject_or_unit_name_1):
            subject_or_unit_desc_1.append('')
        if len(subject_or_unit_object_1) > len(subject_or_unit_name_1):
            subject_or_unit_object_1.append('')

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


        print('///////////////////////////////////////////////////////////////////')
        print('subject name' + str(subject_or_unit_name_1))
        print('subject description' + str(subject_or_unit_desc_1))
        print('subject objective' + str(subject_or_unit_object_1))



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

test_df.to_csv(r'/Users/zeinalabidin/desktop/CSV_files/VictoriaUniversityBachelorCourses1-15.csv', index=False,header=True)

for x in skipped:
    print(x)

    