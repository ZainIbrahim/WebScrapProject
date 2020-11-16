from bs4 import BeautifulSoup
from requests import get
import pandas as pd

url = get('https://www.taxinstitute.com.au/education/single-subjects')
soup = BeautifulSoup(url.text, 'html.parser')
#print(soup.prettify())
links = []
for div_tag in soup.find_all('div', class_='card-main inside-full-height')[1:4]:
    #print(div_tag)
    for i in div_tag.find_all('a'):
        link = i.get('href')
        print(link)
        links.append(link)

# get data
uni_names, country_names, titles, level_codes, descriptions, faculties, int_fees, currencies, cities, local_fees, skipped =([] for i in range(11))
currency_times, durations, duration_times, full_times, part_times, prere1s, prere2s, prere3s, prere1grades,prere2grades,prere3grades = ([] for i in range(11))
linksss, course_langs, availabilities,career_outcomes, onlines, offlines, distances, face_to_faces, blendeds, remarks, course_delivery_modes, free_tafes = ([] for i in range(12))

for q in range(len(links)):
    url2 = get('https://www.taxinstitute.com.au'+links[q])
    urll = 'https://www.taxinstitute.com.au'+links[q]
    soup2 = BeautifulSoup(url2.text, 'html.parser')
    #print(soup2.prettify())

    #title
    div_tag2 = soup2.find('div', class_='container padding-top-xxl padding-bottom-xxl padding-bottom hero-links')
    title = div_tag2.h1.text
    print(title)
    titles.append(title)

    #description
    descriptions_renew = []
    try:
        div_tag3 = soup2.find('div', class_='col-md-8 padding-top')
        for i in div_tag3.find_all('p'):
            desc = i.text
            print(desc)
            descriptions_renew.append(desc)
        descriptions.append(', '.join(descriptions_renew))
    except:
        if soup2.find('div', class_='col-md-8 margin-top'):
            div_tag3 = soup2.find('div', class_='col-md-8 margin-top')
            for i in div_tag3.find_all('p'):
                desc = i.text
                print(desc)
                descriptions_renew.append(desc)
            descriptions.append(', '.join(descriptions_renew))

    '''div_tag4 = soup2.find('div', class_='item')
    for who_for in div_tag4.find_all('li'):
        who_for = who_for.text
        print(who_for)
    '''

    #remarks
    div_tag4 = soup2.find('div', class_='item')
    entry_req = div_tag4.find_all('p')[1].text
    print(entry_req)
    remarks.append(entry_req)

    try:
        learning_outcome = div_tag4.find_all('p')[3].text
        print(learning_outcome)
        career_outcomes.append(learning_outcome)

    except:
        career_outcomes.append('')
        pass


    #int_fees
    try:
        div_tag6 = soup2.find_all('div', class_='item')[5]
        tr_tag = div_tag6.find_all('tr')[1]
        price = tr_tag.find_all('td')[1].text
        print(price)
        int_fees.append(price)
    except:
        div_tag6 = soup2.find_all('div', class_='item')[4]
        tr_tag = div_tag6.find_all('tr')[1]
        price = tr_tag.find_all('td')[1].text
        print(price)
        int_fees.append(price)

    #level code
    level_codes.append('VOC')

    #duration
    if soup2.find(class_='col-md-12 grey-background text-center margin-bottom padding-top'):
        div_dura = soup2.find(class_='col-md-12 grey-background text-center margin-bottom padding-top')
        if "Study length" in div_dura.find_next('p').text:
            p_dura = div_dura.find_next('p').text.split('Study length: ')
            dur1 = p_dura[1].split('Study periods:')
            dur2 = dur1[0].strip()
            print(dur2)
            durations.append(dur2)
        elif "Study Length" in div_dura.find_next('p').text:
            p_dura = div_dura.find_next('p').text.split('Study Length: ')
            dur1 = p_dura[1].split('Study Periods:')
            dur2 = dur1[0].strip()
            print(dur2)
            durations.append(dur2)
    else:
        durations.append('')
    if len(titles) != len(durations):
        durations.append('')

    #location
    cities.append('Sydney')

    #faculty
    faculties.append('Law')

    #course Delivery mode
    course_delivery_modes.append('Normal')

    # set university name
    uni_name = 'The Tax Institute'
    uni_names.append(uni_name)

    # get local fees
    local_fees.append('')

    # set currency
    currencies.append('AUD')

    # set currency_time
    currency_times.append('Year')

    # set duration time
    duration_times.append('Week')

    #full time
    full_times.append('Yes')

    #part time
    part_times.append('')

    # set prerequisite 2
    prere2s.append('')

    # set prerequisite 3
    prere3s.append('')

    # set prerequisite 2 grade
    prere2grades.append('')

    # set prerequisite 3 grade
    prere3grades.append('')

    # set website
    linksss.append(urll)

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
    offline = 'NO'
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

    # prerequisite 1
    prere1s.append('')

    # prerequisite 1 grade
    prere1grades.append('')

    # free tafe
    free_tafes.append('No')

    print('Level code' + str(len(level_codes)))
    print('City' + str(len(cities)))
    print('Courses' + str(len(titles)))
    print('Faculty' + str(len(faculties)))
    print('full time' + str(len(full_times)))
    print('part time' + str(len(part_times)))
    print('Duration' + str(len(durations)))
    print('Description' + str(len(descriptions)))
    print('course delivery mode' + str(len(course_delivery_modes)))
    print('Career outcomes' + str(len(career_outcomes)))
    print('Remarks' + str(len(remarks)))



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
    'Free TAFE': free_tafes
})

test_df.to_csv(r'/Users/zeinalabidin/desktop/CSV_files/The Tax Institute 1.csv', index=False,header=True)
