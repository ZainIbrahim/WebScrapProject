from requests import get
from bs4 import BeautifulSoup
import time
import pandas as pd

uni_names, country_names, titles, level_codes, descriptions, faculties, int_fees, currencies, cities, local_fees =([] for i in range(10))
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
        if soup.find('h2', class_='c-degree-finder__header'):
            title = soup.find('h2', class_='c-degree-finder__header').text.strip()
            print(title)
            titles.append(title)
        else:
            continue
            #print('NO title found')

        #get level code
        if soup.find(class_='c-degree-finder__detail-grid'):
            degree_details = soup.find(class_='c-degree-finder__detail-grid')
            narrow_down = degree_details.find_all(class_='c-degree-finder__detail-grid-item')
            if len(narrow_down) != 0:
                #print(narrow_down)
                for grid_items in narrow_down:
                    for lable in grid_items.find_all(class_='c-degree-finder__detail-grid-label'):
                        if 'Degree' in lable.text:
                            level_code = lable.find_next('span').text
                            ##########################################################################
                            if level_code == 'Bachelor':
                                code = 'BA'
                                level_codes.append(code)
                            elif level_code == 'Diploma':
                                code = 'DIP'
                                level_codes.append(code)
                            elif level_code == 'Undergraduate':
                                code = 'UG'
                                level_codes.append(code)
                            elif level_code == 'Associate Degree':
                                code = 'ADEG'
                                level_codes.append(code)
                            elif level_code == 'Double Degree':
                                code = 'BA'
                                level_codes.append(code)
                            elif level_code == 'Combined Degree':
                                code = 'BA'
                                level_codes.append(code)
                            elif level_code == 'Honours Bachelor':
                                code = 'BAH'
                                level_codes.append(code)
                            elif level_code == 'Vocational':
                                code = 'VOC'
                                level_codes.append(code)
                            elif level_code == 'Certificate I':
                                code = 'CERTI'
                                level_codes.append(code)
                            elif level_code == 'Advanced diploma':
                                code = 'ADIP'
                                level_codes.append(code)
                            elif level_code == 'Foundation':
                                code = 'FOUND'
                                level_codes.append(code)
                            else:
                                level_codes.append(title)
                            ##########################################################################
                            print(level_code)
                        #else:
                        #    level_codes.append(title)
            else:
                level_codes.append(title)
        else:
            level_codes.append(title)

        if len(titles) != len(level_codes):
            level_codes.append(title)

        # set university name
        uni_name = 'The University of Adelaide'
        uni_names.append(uni_name)

        #get city
        city = 'Adelaide'
        if soup.find(class_='c-degree-finder__detail-grid'):
            degree_details = soup.find(class_='c-degree-finder__detail-grid')
            narrow_down = degree_details.find_all(class_='c-degree-finder__detail-grid-item')
            if len(narrow_down) != 0:
                #print(narrow_down)
                for grid_items in narrow_down:
                    for lable in grid_items.find_all(class_='c-degree-finder__detail-grid-label'):
                        if 'Campus' in lable.text:
                            camp = lable.find_next('span').text
                            campus = camp.strip()
                            ################################################################
                            if campus == 'North Terrace Campus':
                                uni_city = 'Adelaide'
                                cities.append(uni_city)
                            elif campus == 'Roseworthy Campus':
                                uni_city = 'Roseworthy'
                                cities.append(uni_city)
                            elif campus == 'Waite Campus':
                                uni_city = 'Urrbrae'
                                cities.append(uni_city)
                            elif campus == 'Melbourne Campus':
                                uni_city = 'Melbourne'
                                cities.append(uni_city)
                            ################################################################
                            print(campus)
            else:
                cities.append(city)
        else:
            cities.append(city)

        if len(titles) != len(cities):
            cities.append(city)

        #get faculty
        if soup.find('nav', class_='nav-breadcrumbs'):
            nav = soup.find('nav', class_='nav-breadcrumbs')
            script = nav.find_next('script')
            script_to_string = str(script)
            if 'faculty' in script_to_string:
                fac = script_to_string.split("'faculty': ")
                fac2 = fac[1].split("},")
                fac3 = fac2[0].strip()
                faculty_code = fac3.replace('"', '')
                ################################################################
                if faculty_code == 'humss':
                    faculty = "Faculty of Arts, Languages, and Social Sciences"
                    faculties.append(faculty)
                elif faculty_code == 'ecms':
                    faculty = "Faculty of Engineering, Computer and Mathematical Sciences"
                    faculties.append(faculty)
                elif faculty_code == 'scifac':
                    faculty = "Faculty of Sciences (Agriculture, Biomedical Sciences, Biotecnology, Earth and Environmental Sciences)"
                    faculties.append(faculty)
                elif faculty_code == 'health':
                    faculty = "Faculty of Health and Medical Sciences"
                    faculties.append(faculty)
                else:
                    faculties.append('')
                ################################################################

                print(faculty_code)

            else:
                faculties.append('')
        else:
            faculties.append('')


        #get duration
        if soup.find(class_='c-degree-finder__detail-grid'):
            degree_details = soup.find(class_='c-degree-finder__detail-grid')
            narrow_down = degree_details.find_all(class_='c-degree-finder__detail-grid-item')
            if len(narrow_down) != 0:
                #print(narrow_down)
                for grid_items in narrow_down:
                    for lable in grid_items.find_all(class_='c-degree-finder__detail-grid-label'):
                        if 'Duration' in lable.text:
                            dur = lable.find_next('span').text.split('year')
                            duration = dur[0].strip()
                            print(duration)
                            durations.append(duration)
            else:
                durations.append('')
        else:
            durations.append('')
        if len(titles) != len(durations):
            cities.append('')

        #get international fees
        li_tag = soup.find_all('li', class_='c-accordion__item')
        #print(li_tag)
        if len(li_tag) != 0:
            for li in li_tag:
                if "Fees" in li.a.text:
                    if li.find('table', class_='ui-table'):
                        if li.find('table', class_='ui-table', summary ='International admissions information'):
                            table_tag = li.find('table', class_='ui-table', summary ='International admissions information')
                            if table_tag.find('tr'):
                                tr_tag = table_tag.find('tr')
                                for td in tr_tag.find_all('td'):
                                    if "$" in td.text:
                                        fe = td.text.split('$')
                                        fee = fe[1].strip()

                                        total_fee = float(fee.replace(',', ''))*float(duration)
                                        print('{:,}'.format(total_fee))
                                        int_fees.append('{:,}'.format(total_fee))
        else:
            int_fees.append('')
        if len(titles) != len(int_fees):
            int_fees.append('')

        #get local fees
        local_fees.append('')

        #set currency
        currencies.append('AUD')

        # set currency_time
        currency_times.append('Year')

        # set duration time
        if float(duration) == 1.0:
            duration_times.append('Year')
        elif float(duration) > 1:
            duration_times.append('Years')

        # set fulltime
        full_times.append('Yes')

        # set parttime
        part_times.append('Yes')

        # get prerequiste 1
        h6_tag = soup.find_all('h6')
        for h6 in h6_tag:
            if 'Prerequisites' in h6.text:
                if h6.find_next('table', class_='c-table c-table--striped'):
                    table_tag2 = h6.find_next('table', class_='c-table c-table--striped')
                    #print(table_tag2)
                    tr_tag = table_tag2.find_all('tr')
                    if len(tr_tag) != 0:
                        prerequisite = table_tag2.tr.th.text
                        if "Australian" in prerequisite:
                            prerequisite_ = prerequisite.replace('Australian', '')
                            prerequisite__= prerequisite_.strip()
                            prere1s.append(prerequisite__)
                            print(prerequisite__)
                        else:
                            prere1s.append(prerequisite)
                            print(prerequisite)

        if len(titles) != len(prere1s):
            prere1s.append('')

        #get preprequisite 2
        h6_tag = soup.find_all('h6')
        for h6 in h6_tag:
            if 'Prerequisites' in h6.text:
                if h6.find_next('table', class_='c-table c-table--striped'):
                    table_tag2 = h6.find_next('table', class_='c-table c-table--striped')
                    #print(table_tag2)
                    tr_tag = table_tag2.find_all('tr')
                    if len(tr_tag) > 1:
                        prereq2 = table_tag2.find_all('tr')[1]
                        prerequisite2 = prereq2.th.text
                        prerequisite2_ = prereq2.th.text.strip()
                        prere2s.append(prerequisite2_)
                        print(prerequisite2_)

        if len(titles) != len(prere2s):
            prere2s.append('')

        # get prerequisite 3
        h6_tag2 = soup.find_all('h6')
        for h6 in h6_tag:
            if "English Language Requirements" in h6.text:
                if h6.find_next('table',class_='c-table c-table--striped'):
                    table_tag3 = h6.find_next('table',class_='c-table c-table--striped')
                    tr = table_tag3.find_all('tr')[1]
                    if tr.find('table', class_='df_int_elr_table'):
                        inside_table = tr.find('table', class_='df_int_elr_table')
                        td1 = inside_table.find_all('td')[0].text
                        print(td1)
                        prere3s.append(td1)
                        #print(tr)

        if len(titles) != len(prere3s):
            prere3s.append('')


        #get prerequisite 1 grade
        prere1grades.append('')

        #get prerequisite 2 grade
        h6_tag = soup.find_all('h6')
        for h6 in h6_tag:
            if 'Prerequisites' in h6.text:
                if h6.find_next('table', class_='c-table c-table--striped'):
                    table_tag2 = h6.find_next('table', class_='c-table c-table--striped')
                    #print(table_tag2)
                    tr_tag = table_tag2.find_all('tr')
                    if len(tr_tag) > 1:
                        prereq2_grade = table_tag2.find_all('tr')[1]
                        prerequisite2_grade = prereq2_grade.td.text
                        prerequisite2_grade_ = prereq2_grade.td.text.strip()
                        prere2grades.append(prerequisite2_grade_)
                        print(prerequisite2_grade_)
        if len(titles) != len(prere2grades):
            prere2grades.append('')

        # get prerequisite 3 grade
        h6_tag2 = soup.find_all('h6')
        for h6 in h6_tag:
            if "English Language Requirements" in h6.text:
                if h6.find_next('table',class_='c-table c-table--striped'):
                    table_tag3 = h6.find_next('table',class_='c-table c-table--striped')
                    tr = table_tag3.find_all('tr')[1]
                    if tr.find('table', class_='df_int_elr_table'):
                        inside_table = tr.find('table', class_='df_int_elr_table')
                        td1 = inside_table.find_all('td')[1].text
                        if "Overall" in td1:
                            prere3_grade = td1.replace("Overall","")
                            prere3_ = prere3_grade.strip()
                            print(prere3_)
                            prere3grades.append(prere3_)
                        #print(tr)

        if len(titles) != len(prere3grades):
            prere3grades.append('')

        #set website
        linksss.append(url)

        #set course language
        course_langs.append('English')

        #get availability
        availabilities.append('A')

        #get course description
        description2_ = None
        description_ = None
        p_tag = soup.find_all('p')
        for p in p_tag:
            if "What will you do?" in p.text:
                description = p.find_next('p').text
                description_ = description.strip()
                #descriptions.append(description_)

            if p.find_next(style = 'list-style-type: disc;'):
                description2 = p.find_next(style = 'list-style-type: disc;')
                description2_ = description2.text.replace("\n","")
                print(description2_)

                    #descriptions.append(description_)
        if description_ is not None and description2_ is not None:
            descriptions.append(description_+'/n'+description2_)
        elif description_ is not None and description2_ is None:
            descriptions.append(description_ )
        elif description_ is None and description2_ is not None:
            descriptions.append(description2_ )


        if len(titles) != len(descriptions):
            descriptions.append('')

        #get career outcomes
        li_tag = soup.find_all('li', class_='c-accordion__item')
        #print(li_tag)
        if len(li_tag) != 0:
            for li in li_tag:
                if "Career" in li.a.text:
                    h4_tag = li.find_all('h4')
                    for h4 in h4_tag:
                        if "Potential careers" in h4.text:
                            careers = h4.find_next('p').text
                            careers_ = careers.replace("\n","")
                            print(careers_)
                            career_outcomes.append(careers_)

        if len(titles) != len(career_outcomes):
            career_outcomes.append('')

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

        #get remarks
        li_tag = soup.find_all('li', class_='c-accordion__item')
        #print(li_tag)
        if len(li_tag) != 0:
            for li in li_tag:
                if "Entry Requirements" in li.a.text:
                    if li.find('div', class_='c-callout'):
                        remarks_content = li.find('div', class_='c-callout').text
                        remark = remarks_content.strip()
                        print(remark)
                        remarks.append(remark)

        if len(titles) != len(remarks):
            remarks.append('')

        print('Level code' + str(len(level_codes)))
        print('City' + str(len(cities)))
        print('Courses' + str(len(titles)))
        print('Faculty' + str(len(faculties)))
        print('Int fees' + str(len(int_fees)))
        print('Duration' + str(len(durations)))
        print('Prerequiste_1' + str(len(prere1s)))
        print('Prerequiste_2' + str(len(prere2s)))
        print('Prerequiste_3' + str(len(prere3s)))
        print('Prerequiste_2_grade' + str(len(prere2grades)))
        print('Prerequiste_3_grade' + str(len(prere3grades)))
        print('Website' + str(len(linksss)))
        print('Description' + str(len(descriptions)))
        print('Career outcomes' + str(len(career_outcomes)))
        print('Remarks' + str(len(remarks)))
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

test_df.to_csv(r'/Users/zeinalabidin/desktop/CSV_files/AdelaideUniversityBachelorCourses201-300.csv', index=False,header=True)