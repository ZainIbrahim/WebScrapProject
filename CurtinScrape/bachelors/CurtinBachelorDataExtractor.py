from requests import get
from bs4 import BeautifulSoup
import time
import pandas as pd

uni_names, country_names, titles, level_codes, descriptions, faculties, int_fees, currencies, cities, local_fees =([] for i in range(10))
currency_times, durations, duration_times, full_times, part_times, prere1s, prere2s, prere3s, prere1grades,prere2grades,prere3grades = ([] for i in range(11))
linksss, course_langs, availabilities,career_outcomes, onlines, offlines, distances, face_to_faces, blendeds, remarks = ([] for i in range(10))
subject_or_unit_name_1, subject_or_unit_name_2, subject_or_unit_name_3, subject_or_unit_name_4, subject_or_unit_name_5, subject_or_unit_name_6, subject_or_unit_name_7, subject_or_unit_name_8, subject_or_unit_name_9, subject_or_unit_name_10 = ([] for i in range(10))
subject_or_unit_desc_1, subject_or_unit_desc_2, subject_or_unit_desc_3, subject_or_unit_desc_4, subject_or_unit_desc_5, subject_or_unit_desc_6, subject_or_unit_desc_7, subject_or_unit_desc_8, subject_or_unit_desc_9, subject_or_unit_desc_10 = ([] for i in range(10))

'''Collect data'''
with open('links.txt') as f:
   for line in f:

        url = line
        #url = 'https://study.curtin.edu.au/offering/course-ug-professional-writing-and-publishing-double-degree-major-babcom--mddu-prwrpv1/'
        #print(url)
        request = get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(request.text, 'html.parser')
        #print(soup.prettify())
        soup2 = None
        # set university name
        uni_name = 'Curtin University'
        print(uni_name)
        uni_names.append(uni_name)

        #set city
        city = 'Perth'
        cities.append(city)
        #get course title
        title = soup.find('h1', class_='hero offering-overview__hero__title').text
        print(title)
        titles.append(title)

        #get course level
        level_codeq = soup.find('title')
        if level_codeq.find_next('script'):
            script_tagq = level_codeq.find_next('script')
            sss = str(script_tagq)
            if sss.split("'fsStudyLvl': '"):
                script_tag_ = sss.split("'fsStudyLvl': '")
                if script_tag_[1].split("',"):
                    script_tag2 = script_tag_[1].split("',")
                    script_tag3 = script_tag2[0]
                    level_code = (script_tag3)
                    if level_code == 'undergraduate':
                        print(level_code)
                        level_codes.append('BA')
                    else:
                        level_codes.append(level_code)
                else:
                    level_codes.append("NULL")
            else:
                level_codes.append("NULL")
        else:
            level_codes.append("NULL")

        faculty = soup.find('title')
        if faculty.find_next('script'):
            script_tag = faculty.find_next('script')
            sss = str(script_tag)
            if sss.split('School'):
                script_tag_ = sss.split("'fsTaughtBy': '")
                if script_tag_[1].split("',"):
                    script_tag2 = script_tag_[1].split("',")
                    script_tag3 = script_tag2[0]
                    faculty_ = (script_tag3)
                    print(faculty_)
                    faculties.append(faculty_)
                else:
                    faculties.append(title)
            else:
                faculties.append("NULL")
        else:
            faculties.append("NULL")

        #get international fees
        if soup.find('section', class_='offering-section content fees-and-charges'):
            section = soup.find('section', class_='offering-section content fees-and-charges')
            if "Please view the" in section.text:
                if "/offering/course" in section.p.find('a').get('href'):
                    parent_link = section.p.a.get('href')
                    parent_url = 'https://study.curtin.edu.au/'+parent_link

                    request2 = get(parent_url)
                    soup2 = BeautifulSoup(request2.text, 'html.parser')
                    #print(soup2.prettify())

                    if soup2.find('section', class_='offering-section content fees-and-charges'):
                        section2 = soup2.find('section', class_='offering-section content fees-and-charges')
                        if section2.find('table'):
                            table_tag = section2.find('table')
                            tbody = table_tag.find('tbody')
                            for tr in tbody.find_all('tr'):
                                if "Total indicative" in tr.text:
                                    fee = tr.find_all('td')[1].text
                                    print(fee)
                                    int_fees.append(fee)
                        else:
                            int_fees.append("NULL")
                    else:
                        int_fees.append("NULL")
                else:
                    int_fees.append("NULL")
                    #continue
                    #False

            elif "International"  in section.text :
                section2 = soup.find('section', class_='offering-section content fees-and-charges')
                table_tag = section2.find('table')
                tbody = table_tag.find('tbody')
                for tr in tbody.find_all('tr'):
                    if "Total indicative" in tr.text:
                        fee = tr.find_all('td')[1].text
                        print(fee)
                        int_fees.append(fee)
            else:
                int_fees.append("NULL")
        else:
           int_fees.append("NULL")


        # get duration within international fees
        if soup.find(class_='offering-overview__details'):
            duration = soup.find(class_='offering-overview__details')
            if duration.find('dd', class_='details-duration'):
                duration_ = duration.find('dd', class_='details-duration').text.split('year')
                dur = duration_[0].strip()
                print(dur)
                durations.append(dur)
            else:
                if soup2 is not None:
                    if soup2.find(class_='offering-overview__details'):
                        duration = soup2.find(class_='offering-overview__details')
                        if duration.find('dd', class_='details-duration'):
                            duration_ = duration.find(class_='details-duration').text.split('year')
                            dur = duration_[0].strip()
                            print(dur)
                            durations.append(dur)
                        else:
                            durations.append("NULL")
                    else:
                        durations.append("NULL")
                else:
                    durations.append("NULL")
        else:
            durations.append('NULL')
        '''
        #if len(titles) != len(durations):
        #    durations.append('NULL')
        
            if duration_ is None:
               
            else:
                durations.append("NULL")
        else:
            durations.append("NULL")
        '''
        #durations.append("NULL")
        #get local fees
        #local_fees.append('')
        # set currency
        currency = 'AUD'
        currencies.append(currency)

        # set currency_time
        currency_time = 'Year'
        currency_times.append(currency_time)

        # set duration time
        duration_time = 'Years'
        duration_times.append(duration_time)

        #set fulltime
        full_time = 'Yes'
        full_times.append(full_time)

        #set parttime
        part_time = 'No'
        part_times.append(part_time)

        #get prerequiste 1
        '''
        prere1ss =[]
        if soup.find('div', class_='table-block'):
            table_block = soup.find('div', class_='table-block')
            if "IELTS" in table_block.find('th').text:

                table2 = table_block.find_next('table')
                tbody2 = table2.find('tbody')
                for tr in tbody2.find_all('tr'):
                    requisite1 = tr.text.strip()
                    print(requisite1)
                    prere1ss.append(requisite1)
                prere1s.append(', '.join(prere1ss))
        '''
        prere1s.append('')
        '''#prerequistie 1 grade
                for tr in tbody2.find_all('tr'):
                    if "Overall" in tr.text:
                        grade = tr.find_all_next('td')[1].text
                        print(grade)
                        prere1grades.append(grade)
            else:
                prere1s.append(" ")
                prere1grades.append(" ")
        else:
            prere1s.append(" ")
            prere1grades.append(" ")
        '''
        prere1grades.append(" ")


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

        # get website
        linksss.append(url)

        #set course language
        course_lang = 'English'
        course_langs.append(course_lang)

        #get availability
        availability = 'A'
        availabilities.append(availability)

        # get course description
        '''
        if soup.find(class_='offering__sections'):
            bb = soup.find(class_='offering__sections')
            if bb.find(class_='outline__content content reduced' ):
                description = bb.find(class_='outline__content content reduced' )
                description_ = description.find_next('p').text
                print(description_)
                descriptions.append(description_)
            else:
                descriptions.append("NULL")

        elif soup.find(class_='outline__lead hero-intro last-mb0'):
            description = soup.find(class_='outline__lead hero-intro last-mb0').text.strip()
            print(description)
            descriptions.append(description)

        elif soup.find(class_='outline__lead hero-intro last-mb0') and soup.find(class_='outline__content content  reduced') is not True:
            for h3_tagg in  soup.find_all('h3'):
             if "What you" in h3_tagg:
                 h333 = h3_tagg.find_next('ul').li.text
                 print(h333)
                 descriptions.append(h333)
        else:
            descriptions.append("NULL")
        '''
        descriptions.append("")

        #career outcomes
        career_renew =[]
        h3_tag = soup.find_all('h3')
        for h3 in h3_tag:
            if 'Career information' in h3.text:
                    career = h3.find_next('p')
                    if career.text.startswith('Career'):
                        career_= career.find_next('ul')
                        for li in career_.find_all('li'):
                            career__ = li.text
                            print(career__)
                            career_renew.append(career__)
                            print(career_renew)
                        career_outcomes.append(', '.join(career_renew))

                    else:
                        career_ = career.text
                        print(career_)
                        career_outcomes.append(career_)

        if len(titles) != len(career_outcomes):
            career_outcomes.append("NULL")

        # set country
        country = 'Australia'
        print(country)
        country_names.append(country)

        #online
        online = 'Yes'
        onlines.append(online)
        #offline
        offline = 'Yes'
        offlines.append(offline)
        #distance
        distance = ''
        distances.append(distance)
        #face-to-face
        if offline is 'Yes':
            face_to_faces.append('Yes')
        else:
            face_to_faces.append('NO')
        #blended
        if online and offline == 'Yes':
            blendeds.append('Yes')
        else:
            blendeds.append("NO")

        #remarks
        if soup.find(class_='offering-section__title'):
            remark = soup.find(class_='offering-section__title')
            p_tag = remark.find_next('p').text
            print(p_tag)
            remarks.append(p_tag)
        else:
            remarks.append('NULL')

        '''=============================Subject names, descriptions ================================='''
        #get the first set of links
        first_set_link = []
        div_tagz = soup.find(class_='outline__links-wrap')
        if div_tagz:
            for li in div_tagz.ul.find_all('li'):
                #print('this is li: '+str(li))
                for a in li.find_all('a'):
                    if 'handbook.curtin.edu.au' in a.get('href'):
                        #print(a.get('href'))
                        first_set_link.append(a.get('href'))

        if len (first_set_link) == 0:
            subject_or_unit_name_1.append('')
            subject_or_unit_name_2.append('')
            subject_or_unit_name_3.append('')
            subject_or_unit_name_4.append('')
            subject_or_unit_name_5.append('')
            subject_or_unit_name_6.append('')
            subject_or_unit_name_7.append('')
            subject_or_unit_name_8.append('')
            subject_or_unit_name_9.append('')
            subject_or_unit_name_10.append('')
            subject_or_unit_desc_1.append('')
            subject_or_unit_desc_2.append('')
            subject_or_unit_desc_3.append('')
            subject_or_unit_desc_4.append('')
            subject_or_unit_desc_5.append('')
            subject_or_unit_desc_6.append('')
            subject_or_unit_desc_7.append('')
            subject_or_unit_desc_8.append('')
            subject_or_unit_desc_9.append('')
            subject_or_unit_desc_10.append('')

        #get the second set of links
        second_set_links = []
        for x in first_set_link:
            url3 = x
            request3 = get(url3, headers={'User-Agent': 'Mozilla/5.0'})
            soup3 = BeautifulSoup(request3.text, 'html.parser')

            table_tagz = soup3.find('table', class_='fullwidth')
            if table_tagz:
                for tr in table_tagz.find_all('tr'):
                    for a in tr.find_all('a'):
                        if len(second_set_links)==10:
                            break
                        linkz = a.get('href').replace('../../','')
                        linkz_ = 'http://handbook.curtin.edu.au/'+linkz
                        #print(linkz_)
                        second_set_links.append(linkz_)


        if len(second_set_links) == 0:
            if len(first_set_link) == 0:
                pass
            else:
                subject_or_unit_name_1.append('')
                subject_or_unit_name_2.append('')
                subject_or_unit_name_3.append('')
                subject_or_unit_name_4.append('')
                subject_or_unit_name_5.append('')
                subject_or_unit_name_6.append('')
                subject_or_unit_name_7.append('')
                subject_or_unit_name_8.append('')
                subject_or_unit_name_9.append('')
                subject_or_unit_name_10.append('')
                subject_or_unit_desc_1.append('')
                subject_or_unit_desc_2.append('')
                subject_or_unit_desc_3.append('')
                subject_or_unit_desc_4.append('')
                subject_or_unit_desc_5.append('')
                subject_or_unit_desc_6.append('')
                subject_or_unit_desc_7.append('')
                subject_or_unit_desc_8.append('')
                subject_or_unit_desc_9.append('')
                subject_or_unit_desc_10.append('')
        #get the data
        subject_names = []
        subject_descriptions = []
        subject_objectives = []
        for h in second_set_links:
            url4 = h
            request4 = get(url4, headers={'User-Agent': 'Mozilla/5.0'})
            soup4 = BeautifulSoup(request4.text, 'html.parser')

            #get the title
            subject_name_renew = []
            div_tagz = soup4.find(id= 'breadcrumbs')
            title_tagz = div_tagz.find_next('h1').text.strip()
            print('this is the titles of the course: ' + title_tagz)
            subject_name_renew.append(title_tagz)

            #get course description
            subject_description_renew = []
            for th in soup4.find_all('th'):
                if 'Syllabus:' in th.text:
                    td_tagz = th.find_next('td').text
                    print('this is the course description: ' +td_tagz)
                    subject_description_renew.append(td_tagz)


            subject_names.append(', '.join(subject_name_renew))
            subject_descriptions.append(', '.join(subject_description_renew))
            time.sleep(1.5)

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





        print( 'Level code'+ str(len( level_codes)))
        print('University'+ str(len(uni_names)))
        print('City'+ str(len( cities)))
        print('Courses'+ str(len( titles)))
        print('Faculty'+ str(len( faculties)))
        print('Int fees'+ str(len( int_fees)))
        print('Currency'+ str(len( currencies)))
        print( 'Currency Time'+ str(len( currency_times)))
        print( 'Duration'+ str(len( durations)))
        print('Duration Time'+ str(len( duration_times)))
        print('Prerequiste_1'+ str(len( prere1s)))
        print( 'Prerequiste_2'+ str(len( prere2s)))
        print( 'Prerequiste_3'+ str(len( prere3s)))
        print( 'Prerequiste_1_grade'+ str(len( prere1grades)))
        print( 'Prerequiste_2_grade'+ str(len( prere2grades)))
        print('Prerequiste_3_grade'+ str(len( prere3grades)))
        print('Website'+ str(len( linksss)))
        print('course_lang'+ str(len( course_langs)))
        print( 'Availability'+ str(len( availabilities)))
        print( 'Description'+ str(len( descriptions)))
        print( 'Career outcomes'+ str(len( career_outcomes)))
        print('Country'+ str(len( country_names)))
        print('Online'+ str(len( onlines)))
        print('Offline'+ str(len( offlines)))
        print('Distance'+ str(len( distances)))
        print('Face to face'+ str(len( face_to_faces)))
        print( 'Blended'+ str(len( blendeds)))
        print( 'Remarks'+ str(len( remarks)))
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

        print('====================================================================================================================')
        #time.sleep(3)
test_df = pd.DataFrame({
    'Level code' : level_codes,
    'University' : uni_names,
    'City': cities,
    'Courses': titles,
    'Faculty': faculties,
    'Int fees': int_fees,
    'Currency': currencies,
    'Currency Time': currency_times,
    'Duration' : durations,
    'Duration Time' :duration_times,
    'Prerequiste_1': prere1s,
    'Prerequiste_2': prere2s,
    'Prerequiste_3': prere3s,
    'Prerequiste_1_grade': prere1grades,
    'Prerequiste_2_grade': prere2grades,
    'Prerequiste_3_grade': prere3grades,
    'Website' : linksss,
    'course_lang' : course_langs,
    'Availability' : availabilities,
    'Description': descriptions,
    'Career outcomes': career_outcomes,
    'Country': country_names,
    'Online': online,
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

})


test_df.to_csv(r'/Users/zeinalabidin/desktop/CSV_files/CurtinUniversityBachelorCourses255-305.csv', index = False, header=True)