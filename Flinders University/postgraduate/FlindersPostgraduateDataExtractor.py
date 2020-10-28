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
        '''if soup.find(class_='yellow_heading'):
            title = soup.find(class_='yellow_heading').text
            titles.append(title)
            print(title)
        else:
            skipped.append(url)
            continue
        '''


        title = None
        if soup.find(class_="component_section international_grey_container international_grey_container_featured section_component_updated padding_top_50 padding_bottom_50 padding_left_none padding_right_none transparency_none viewport_auto international_content col_3_section"):
            div_tag = soup.find(class_="component_section international_grey_container international_grey_container_featured section_component_updated padding_top_50 padding_bottom_50 padding_left_none padding_right_none transparency_none viewport_auto international_content col_3_section")
            #print(div_tag)
            col_md_4 = div_tag.find_all(class_='col-md-4')
            if len(col_md_4) >1:
                #for col in col_md_4[1]:
                col_md_4 = div_tag.find_all(class_='col-md-4')[1]
                if col_md_4.find(class_='text_size_large'):

                    #get title
                    title= col_md_4.find(class_='text_size_large').text
                    print(title)
                    titles.append(title)

                    #get duration
                    duration = col_md_4.find_all('p')
                    for dur in duration:
                        if 'Duration' in dur.text:
                            durr = dur.text.strip()
                            dur1= durr.split('Duration:')
                            dur2 = dur1[1].split('year')
                            dur3 = dur2[0]
                            print(dur3)
                            durations.append(dur3)

                    #get int fees
                    annaul_fee= col_md_4.find_all('p')
                    for fee in annaul_fee:
                        if "Annual" in fee.text:
                            fe = fee.text.split('$')
                            fe1 = fe[1]
                            if '2021' in fe1:
                                fe2 = fe1.split('2021')
                                fe3 = fe2[0]
                                print(fe3)
                                int_fees.append(fe3)
                            else:
                                print(fe1)
                                int_fees.append(fe1)


        #print(div_tag)
        if soup.find(class_='component_section international_grey_container international_grey_container_featured section_component_updated padding_top_50 padding_bottom_50 padding_left_none padding_right_none transparency_none viewport_auto international_content col_2_section'):
            div_tag2 = soup.find(class_='component_section international_grey_container international_grey_container_featured section_component_updated padding_top_50 padding_bottom_50 padding_left_none padding_right_none transparency_none viewport_auto international_content col_2_section')
            col_lg_6 = div_tag2.find_all(class_='col-lg-12')
            if col_lg_6 != 0:
                for col in col_lg_6:
                    if col.find(class_='text_size_large'):

                        # get title
                        title = col.find(class_='text_size_large').text
                        print(title)
                        titles.append(title)

                        # get duration
                        duration = col.find_all('p')
                        for dur in duration:
                            if 'Duration' in dur.text:
                                durr = dur.text.strip()
                                dur1 = durr.split('Duration:')
                                dur2 = dur1[1].split('year')
                                dur3 = dur2[0]
                                print(dur3)
                                durations.append(dur3)

                        # get int fees
                        annaul_fee = col.find_all('p')
                        for fee in annaul_fee:
                            if "Annual" in fee.text:
                                fe = fee.text.split('$')
                                fe1 = fe[1]
                                if '2021' in fe1:
                                    fe2 = fe1.split('2021')
                                    fe3 = fe2[0]
                                    print(fe3)
                                    int_fees.append(fe3)
                                else:
                                    print(fe1)
                                    int_fees.append(fe1)

        # get level code
        if 'Master' in title:
            code = 'MST'
            level_codes.append(code)
        elif 'Foundation' in title:
            code = 'FOUND'
            level_codes.append(code)
        else:
            level_codes.append("")

        # set university name
        uni_name = 'Flinders University'
        uni_names.append(uni_name)

        # get course description
        h2_tag = soup.find_all('h2')
        for h2 in h2_tag:
            if 'Overview' in h2.text:
                cmp_text = h2.find_next(class_="cmp-text").text.strip()
                print(cmp_text)
                descriptions.append(cmp_text)
            # get career outcomes
            if "Your career" in h2.text:
                cmp_text_career = h2.find_next(class_="cmp-text").text.strip()
                print(cmp_text_career)
                career_outcomes.append(cmp_text_career)

        # get faculty
        if soup.find(class_='jotform-form parbase'):
            div_tag2 = soup.find(class_='jotform-form parbase')
            script = div_tag2.find_all_next('script')
            if script != None:
                script_ = div_tag2.find_all_next('script')[1]
                script_to_string = str(script_)
                if 'courseStudyArea' in script_to_string:
                    fac = script_to_string.split('courseStudyArea":"')
                    fac2 = fac[1]
                    fac22 = fac2.split('"},')
                    fac3 = fac22[0].strip()
                    # faculty_code = fac3.replace('"', '')
                    print(fac3)
                    faculties.append(fac3)
        if len(titles) != len(faculties):
            faculties.append('')
        # set city
        cities.append('Adelaide')

        # get local fees
        local_fees.append('')

        # set currency
        currencies.append('AUD')

        # set currency_time
        currency_times.append('Year')

        # set duration time
        duration_times.append('Year')

        # set fulltime
        full_times.append('Yes')

        # set parttime
        part_times.append('Yes')

        # set prerequisite 1
        prere1s.append('Bachelor degree')

        # set prerequisite 2
        prere2s.append('')

        # set prerequisite 3
        prere3s.append('')

        # set prerequisite 1 grade
        prere1grades.append('')

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

        #remarks
        remarks.append('')

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


        if len(linksss) != len(titles):
            titles.append('')
        if len(linksss) != len(durations):
            durations.append('')
        if len(linksss) != len(int_fees):
            int_fees.append('')

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
    print('duration' +str(durations))
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
test_df.to_csv(r'/Users/zeinalabidin/desktop/CSV_files/FlindersUniversityPostgraduateCourses1-20.csv', index=False,header=True)
