from requests import get
from bs4 import BeautifulSoup
import time
import pandas as pd

uni_names, country_names, titles, level_codes, descriptions, faculties, int_fees, currencies, cities, local_fees = ([]for i in range(10))
currency_times, durations, duration_times, full_times, part_times, prere1s, prere2s, prere3s, prere1grades, prere2grades, prere3grades = ([] for i in range(11))
linksss, course_langs, availabilities, career_outcomes, onlines, offlines, distances, face_to_faces, blendeds, remarks = ([] for i in range(10))

'''Collect data'''
with open('links.txt') as f:
    for line in f:

        url = line
        #url = 'https://search.curtin.edu.au/s/redirect?collection=curtin-learning-offerings&url=https%3A%2F%2Fstudy.curtin.edu.au%2Foffering%2Fcourse-pg-graduate-diploma-in-food-science-and-technology--gd-foodstv1&index_url=http%3A%2F%2Fcourse-pg-graduate-diploma-in-food-science-and-technology--gd-foodstv1&auth=wzUA0HCGMZYmivVvqVAYwg&profile=_default&rank=1&query=%21padrenull+%7CstudyArea%3A%22%24%2B%2B+agriculture-environment-and-sustainability+%24%2B%2B%22+%7CofferingLevel%3A%22%24%2B%2B+POSTGRADUATE+%24%2B%2B%22+%7CofferingType%3A%22%24%2B%2B+COURSE+%24%2B%2B%22'
        # print(url)
        request = get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(request.text, 'html.parser')
        #print(soup.prettify())
        soup2 = None



        # get course title
        if soup.find('h1', class_='hero offering-overview__hero__title'):
            title = soup.find('h1', class_='hero offering-overview__hero__title').text
            print(title)
            titles.append(title)
        else:
            continue
        # set university name
        uni_name = 'Curtin University'
        print(uni_name)
        uni_names.append(uni_name)

        # set city
        city = 'Perth'
        cities.append(city)

        # get course level
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
                    if level_code == 'postgraduate':
                        print(level_code)
                        level_codes.append('PG')
                    else:
                        level_codes.append(level_code)
                else:
                    level_codes.append(" ")
            else:
                level_codes.append(" ")
        else:
            level_codes.append(" ")

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
                faculties.append(" ")
        else:
            faculties.append(" ")

        # get international fees
        if soup.find('section', class_='offering-section content fees-and-charges'):
            section = soup.find('section', class_='offering-section content fees-and-charges')

            if "International" in section.text:
                if section.find('table'):
                    table_tag = section.find('table')
                    #print(table_tag)
                    tbody = table_tag.find('tbody')
                    tr =  tbody.find_all('tr')
                    #print(tr)
                    if len(tr) == 3:
                        trr = tr[1]
                        fee = trr.find_all('td')[1].text
                        fee_formatted = fee.replace('*', "").replace("$", '')
                        print(fee_formatted)
                        int_fees.append(fee_formatted)
                    elif len(tr) == 2:
                        trr= tr[1]
                        fee = trr.find_all('td')[1].text
                        fee_formatted = fee.replace('*', "").replace("$", '')
                        print(fee_formatted)
                        int_fees.append(fee_formatted)
                    elif len(tr) ==1:
                        trr= tr[0]
                        fee = trr.find_all('td')[1].text
                        fee_formatted = fee.replace('*', "").replace("$", '')
                        print(fee_formatted)
                        int_fees.append(fee_formatted)
                    else:
                        int_fees.append(" ")
                else:
                    int_fees.append(" ")

            elif "Please view the" in section.text:
                if "/offering/course" in section.p.find('a').get('href'):
                    parent_link = section.p.a.get('href')
                    parent_url = 'https://study.curtin.edu.au/' + parent_link

                    request2 = get(parent_url)
                    soup2 = BeautifulSoup(request2.text, 'html.parser')
                    # print(soup2.prettify())

                    if soup2.find('section', class_='offering-section content fees-and-charges'):
                        section2 = soup2.find('section', class_='offering-section content fees-and-charges')
                        if section2.find('table'):
                            table_tag = section2.find('table')
                            tbody = table_tag.find('tbody')
                            for tr in tbody.find_all('tr'):
                                if "Total indicative" in tr.text:
                                    fee = tr.find_all('td')[1].text
                                    fee_formatted = fee.replace('*', "").replace("$", '')
                                    print(fee_formatted)
                                    int_fees.append(fee_formatted)
                        else:
                            int_fees.append(" ")
                    else:
                        int_fees.append(" ")
                else:
                    int_fees.append(" ")
            else:
                int_fees.append(" ")
        else:
            int_fees.append(" ")

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
                            durations.append(" ")
                    else:
                        durations.append(" ")
                else:
                    durations.append(" ")
        else:
            durations.append(' ')

        # get local fees
        local_fee = ' '
        local_fees.append(local_fee)

        # set currency
        currency = 'AUD'
        currencies.append(currency)

        # set currency_time
        currency_time = 'Year'
        currency_times.append(currency_time)

        # set duration time
        duration_time = 'Years'
        duration_times.append(duration_time)

        # set fulltime
        full_time = 'Yes'
        full_times.append(full_time)

        # set parttime
        part_time = 'No'
        part_times.append(part_time)

        # get prerequiste 1
        prere1ss = []
        if soup.find('div', class_='table-block'):
            table_block = soup.find('div', class_='table-block')
            if "IELTS" in table_block.find('th').text:

                table2 = table_block.find_next('table')
                tbody2 = table2.find('tbody')
                for tr in tbody2.find_all('tr'):
                    requisite1 = tr.text.strip().replace("\n","")
                    print(requisite1)
                    prere1ss.append(requisite1)
                prere1s.append(', '.join(prere1ss))

                # prerequistie 1 grade
                for tr in tbody2.find_all('tr'):
                    if "Overall" in tr.text:
                        grade = tr.find_all_next('td')[1].text
                        grade_ = 'IELTS band: '+grade
                        print(grade_)
                        prere1grades.append(grade_)
            else:
                prere1s.append(" ")
                prere1grades.append(" ")
        else:
            prere1s.append(" ")
            prere1grades.append(" ")


        # prerequisite 2
        prere2 = ''
        prere2s.append(prere2)
        # prerequisite 2 grade
        prere2grade = ''
        prere2grades.append(prere2grade)
        # prerequisite 3
        prere3 = ''
        prere3s.append(prere3)
        # prerequisite 3 grade
        prere3grade = ''
        prere3grades.append(prere3grade)

        # get website
        linksss.append(url)

        # set course language
        course_lang = 'English'
        course_langs.append(course_lang)

        # get availability
        availability = 'A'
        availabilities.append(availability)

        # get course description
        h3_tagg = soup.find_all('h3')#variable for one of the conditions below
        if soup.find(class_='outline__lead hero-intro last-mb0'):
            description = soup.find(class_='outline__lead hero-intro last-mb0').text.strip()
            print(description)
            descriptions.append(description)
        elif soup.find(class_='offering__sections'):
            bb = soup.find(class_='offering__sections')
            if bb.find(class_='outline__content content reduced'):
                description = bb.find(class_='outline__content content reduced')
                description_ = description.find_next('p').text
                print(description_)
                descriptions.append(description_)

        elif "What you" in h3_tagg:
            h333 = h3_tagg.find_next('ul').li.text
            print(h333)
            descriptions.append(h333)
        else:
            descriptions.append(" ")

        # career outcomes
        career_renew = []
        h3_tag = soup.find_all('h3')
        for h3 in h3_tag:
            if 'Career information' in h3.text:
                career = h3.find_next('p')
                if career.text.startswith('Career'):
                    career_ = career.find_next('ul')
                    for li in career_.find_all('li'):
                        career__ = li.text
                        print(career__)
                        career_renew.append(career__)
                    career_outcomes.append(', '.join(career_renew))

                else:
                    career_ = career.text
                    print(career_)
                    career_outcomes.append(career_)

        if len(titles) != len(career_outcomes):
            career_outcomes.append(" ")

        # set country
        country = 'Australia'
        print(country)
        country_names.append(country)

        # online
        online = 'Yes'
        onlines.append(online)

        # offline
        offline = 'Yes'
        offlines.append(offline)

        # distance
        distance = ''
        distances.append(distance)

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
        if soup.find(class_='offering-section__title'):
            remark = soup.find(class_='offering-section__title')
            p_tag = remark.find_next('p').text
            print(p_tag)
            remarks.append(p_tag)
        else:
            remarks.append(' ')

        print('Level code' + str(len(level_codes)))
        print('University' + str(len(uni_names)))
        print('City' + str(len(cities)))
        print('Courses' + str(len(titles)))
        print('Faculty' + str(len(faculties)))
        print('Int fees' + str(len(int_fees)))
        print('Local fees' + str(len(local_fees)))
        print('Currency' + str(len(currencies)))
        print('Currency Time' + str(len(currency_times)))
        print('Duration' + str(len(durations)))
        print('Duration Time' + str(len(duration_times)))
        print('Prerequiste_1' + str(len(prere1s)))
        print('Prerequiste_2' + str(len(prere2s)))
        print('Prerequiste_3' + str(len(prere3s)))
        print('Prerequiste_1_grade' + str(len(prere1grades)))
        print('Prerequiste_2_grade' + str(len(prere2grades)))
        print('Prerequiste_3_grade' + str(len(prere3grades)))
        print('Website' + str(len(linksss)))
        print('course_lang' + str(len(course_langs)))
        print('Availability' + str(len(availabilities)))
        print('Description' + str(len(descriptions)))
        print('Career outcomes' + str(len(career_outcomes)))
        print('Country' + str(len(country_names)))
        print('Online' + str(len(onlines)))
        print('Offline' + str(len(offlines)))
        print('Distance' + str(len(distances)))
        print('Face to face' + str(len(face_to_faces)))
        print('Blended' + str(len(blendeds)))
        print('Remarks' + str(len(remarks)))
        print('fees of internationals' +str(int_fees))


        print('====================================================================================================================')
        # time.sleep(3)

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

test_df.to_csv(r'/Users/zeinalabidin/desktop/CSV_files/CurtinUniversityPostgraduateCourses201-248.csv', index=False,header=True)