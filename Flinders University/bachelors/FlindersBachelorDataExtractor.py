from requests import get
from bs4 import BeautifulSoup
import time
import pandas as pd
from PyPDF2 import PdfFileReader

uni_names, country_names, titles, level_codes, descriptions, faculties, int_fees, currencies, cities, local_fees, skipped =([] for i in range(11))
currency_times, durations, duration_times, full_times, part_times, prere1s, prere2s, prere3s, prere1grades,prere2grades,prere3grades = ([] for i in range(11))
linksss, course_langs, availabilities,career_outcomes, onlines, offlines, distances, face_to_faces, blendeds, remarks = ([] for i in range(10))

'''Collect data'''
with open('links.txt') as f:
    for line in f:

        url = line
        #url = 'https://www.adelaide.edu.au/degree-finder/2021/barta_bartadv.html#df-acc-admission'
        request = get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(request.text, 'html.parser')
        #print(soup.prettify())

        #get title
        if soup.find(class_='yellow_heading'):
            title = soup.find(class_='yellow_heading').text
            titles.append(title)
            print(title)
        else:
            skipped.append(url)
            continue

        #get level code
        if 'Bachelor' in title and 'Honours' in title:
            code = 'BAH'
            level_codes.append(code)
        elif 'Bachelor' in title:
            code = 'BA'
            level_codes.append(code)
        elif 'Undergraduate' in title:
            code = 'UG'
            level_codes.append(code)
        elif 'Foundation' in title:
            code = 'FOUND'
            level_codes.append(code)
        else:
            level_codes.append("BA")

        print(code)

        # set university name
        uni_name = 'Flinders University'
        uni_names.append(uni_name)

        #get city
        if soup.find(class_='ff-tab-content international_content'):
            div_tag= soup.find(class_='ff-tab-content international_content')
            col_sm_6 = div_tag.find_all(class_='col-sm-6')
            for campus in col_sm_6:
                if "Delivery" in campus.text:
                    if campus.find(class_='content_list'):
                        ul_campus = campus.find(class_='content_list')
                        li_campus = ul_campus.li.text
                        if '–' in li_campus:
                            li_cam = li_campus.replace('–', '')
                            campus_ = li_cam.strip()
                            #print(campus_)

                        if campus_ == 'Bedford Park':
                            city = 'Bedford Park'
                            print(city)
                            cities.append(city)
                        elif campus_ == 'Tonsley':
                            city  = 'Tonsley'
                            print(city)
                            cities.append(city)
        if len(titles) != len(cities):
            cities.append('')

        #get duration
        dur = None
        if soup.find(class_='ff-tab-content international_content'):
            div_tag= soup.find(class_='ff-tab-content international_content')
            col_sm_6 = div_tag.find_all(class_='col-sm-6')
            for duration in col_sm_6:
                if "Duration" in duration.text:
                    if duration.find('p'):
                        if duration.find('p'):
                            dur = duration.find('p').text
                            if 'year' in dur:
                                dur_ = dur.split('year')
                                dur__ = dur_[0].strip()
                                print(dur__)
                                durations.append(dur__)
                            elif 'month' in dur:
                                dur_ = dur.split('month')
                                dur__ = dur_[0].strip()
                                print(dur__)
                                durations.append(dur__)

        if len(titles) != len(durations):
            durations.append('')

        #get international fees
        if soup.find(class_='ff-tab-content international_content'):
            div_tag= soup.find(class_='ff-tab-content international_content')
            col_sm_6 = div_tag.find_all(class_='col-sm-6')
            for fee in col_sm_6:
                if "Annual fee" in fee.text:
                    ul_fees = fee.find(class_='content_list')
                    li_fees = ul_fees.find_all('li')
                    for li in li_fees:
                        if '2021' in li.text:
                            li_fees_ = li.text
                            if "$" in li_fees_:
                                li_fees__ = li_fees_.split('$')
                                int_fee = li_fees__[1].strip()
                                print(int_fee)
                                int_fees.append(int_fee)

        if len(titles) != len(int_fees):
            int_fees.append('')

        # set prerequisite 1
        if soup.find(class_='ff-tab-content international_content'):
            div_tag= soup.find(class_='ff-tab-content international_content')
            if div_tag.find(class_='english-reqs content_container'):
                english_req = div_tag.find(class_='english-reqs content_container')
                if english_req.find(class_='english-reqs__title content_header'):
                    prerequisite1 = 'IELTS'
                    prere1s.append(prerequisite1)
        if len (titles) != len(prere1s):
            prere1s.append('')

        #get prerequisite 1 grade
        if soup.find(class_='ff-tab-content international_content'):
            div_tag= soup.find(class_='ff-tab-content international_content')
           # if div_tag.find(class_='english-reqs content_container'):
            #    english_req = div_tag.find(class_='english-reqs content_container')
             #   print(english_req)
            if div_tag.find('div', calss_='english-reqs__title content_header'):
                print('iamgood')
                    #score = eng.find(calss_='english-reqs__score english-reqs__score--large').text
                    #print(score)
                    #prere1grades.append(score)

        prere1grades.append('6')

        #get faculty
        if soup.find(class_='jotform-form parbase'):
            div_tag2 = soup.find(class_='jotform-form parbase')
            script = div_tag2.find_all_next('script')
            if script != None:
                script_= div_tag2.find_all_next('script')[1]
                script_to_string = str(script_)
                if 'courseStudyArea' in script_to_string:
                    fac = script_to_string.split('courseStudyArea":"')
                    fac2 = fac[1]
                    fac22 = fac2.split('"},')
                    fac3 = fac22[0].strip()
                    #faculty_code = fac3.replace('"', '')
                    print(fac3)
                    faculties.append(fac3)
        if len(titles) != len(faculties):
            faculties.append('')

        # get local fees
        local_fees.append('')

        # set currency
        currencies.append('AUD')

        # set currency_time
        currency_times.append('Year')

        # set duration time
        if dur is not None:
            if 'year' in dur:
                if float(dur__) == 1.0:
                    duration_times.append('Year')
                elif float(dur__) > 1:
                    duration_times.append('Years')
            elif 'month' in dur:
                if float(dur__) == 1.0:
                    duration_times.append('Month')
                elif float(dur__) > 1:
                    duration_times.append('Months')

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

        #get course description
        if soup.find(class_='col-md-8 deepest-column no-image-column'):
            description = soup.find(class_='col-md-8 deepest-column no-image-column').text.strip()
            print(description)
            descriptions.append(description.replace('\n',''))
        if len(descriptions) != len(titles):
            descriptions.append('')

        #get career outcomes
        careers = []
        p_tag = soup.find_all('p')
        for p in p_tag:
            if "Potential occupations include" in p.text:
                ul_tag = p.find_next('ul')
                li_tag = ul_tag.find_all('li')
                for li in li_tag:
                    career = li.text
                    careers.append(career)
                career_outcomes.append(', '.join(careers))

        h3_tag = soup.find_all('h3')
        for h3 in h3_tag:
            if "Potential occupations include" in h3.text:
                ul_tag_ = h3.find_next('ul')
                li_tag_ = ul_tag_.find_all('li')
                for li in li_tag_:
                    career = li.text
                    careers.append(career)
                career_outcomes.append(', '.join(careers))

        if len(career_outcomes) > len(titles):
            career_outcomes.pop

        elif len(career_outcomes) < len(titles):
            career_outcomes.append('')

        print(career_outcomes)

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
        remarks_renew =[]
        h3_remarks = soup.find_all('h3')
        for h3 in h3_remarks:
            if "What you will need" in h3.text:
                ul_tag_ = h3.find_next('ul')
                li_tag_ = ul_tag_.find_all('li')
                for li in li_tag_:
                    remark = li.text
                    remarks_renew.append(remark)
                remarks.append(', '.join(remarks_renew))
                print(remarks)
        if len(titles) != len(remarks):
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
        print('skipped urls are: '+str(skipped))
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
        'Online': online,
        'Offline': offlines,
        'Distance': distances,
        'Face to face': face_to_faces,
        'Blended': blendeds,
        'Remarks': remarks
    })

test_df.to_csv(r'/Users/zeinalabidin/desktop/CSV_files/FlindersUniversityBachelorCourses151-184.csv', index=False,header=True)

