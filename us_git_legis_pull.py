
#> This program pulls classifiers and terms of all congresspeople. This includes federal bioguide,
#> opensecrets id, and icpsr.

import urllib.request
# import requests
import json
import pprint
import pandas as pd
import csv

def leg_pull(item):

    final_url = item

    #. Pretend to be Mozilla. This might need to be updated.
    #. Make a variable for the request when a specific url.
    req = urllib.request.Request(final_url, headers={'User-Agent': 'Mozilla/5.0'})

    #. Open this variable and assign it to a new variable
    return_value = urllib.request.urlopen(req)
    body = return_value.read()

    #. Gives us a status code for how the pull went, then what the type of data it is.
    print('Status Check! ', return_value.status)
    print('--------------------------------------')
    # print(type(body))


    #. Decode to utf-8 by default
    decoded_body = body.decode('utf-8')
    # print(decoded_body)
    decoded_body = json.loads(decoded_body)
    # print(type(decoded_body))

    term_results = []
    for x in decoded_body:
        my_dict = {}
        my_dict['bioguide']=x.get('id').get('bioguide')
        my_dict['opensecrets']=x.get('id').get('opensecrets')
        my_dict['icpsr']=x.get('id').get('icpsr')
        my_dict['first']=x.get('name').get('first')
        my_dict['last']=x.get('name').get('last')
        my_dict['first_last']=x.get('name').get('official_full')
        y_iter = 1
        for y in x['terms']:
            my_dict2 = {}
            my_dict2['bioguide'] = my_dict['bioguide']
            my_dict2['opensecrets'] = my_dict['opensecrets']
            my_dict2['icpsr'] = my_dict['icpsr']
            my_dict2['first'] = my_dict['first']
            my_dict2['last'] = my_dict['last']
            my_dict2['first_last'] = my_dict['first_last']
            my_dict2['term_count'] = y_iter
            my_dict2['type'] = y.get('type')
            my_dict2['term_start'] = y.get('start')
            my_dict2['term_end'] = y.get('end')
            y_iter +=1
            # print(my_dict2)
            term_results.append(my_dict2)


    print('Count: ', len(term_results))
    print('--------------------------------------')
    print('Example:')
    print(term_results[:1])
    print(' ')
    print(' ')

    #. This needs to placed into a dataframe because otherwise it's a list and breaks
    term_results = pd.DataFrame(term_results)
    term_results['term_end'] = pd.to_datetime(term_results['term_end'])
    term_results['term_start'] = pd.to_datetime(term_results['term_start'])


    #> No dupes found. Drop all congresspeople that started before 2010
    #. First let's make a mask to limit start dates to before 2010
    mask_start = (term_results['term_start'] > '2010-01-01')
    #. Create a new dataframe = to the mask to term_results
    temp_mask = term_results.loc[mask_start]
    #. Now make a mask to limit term end dats to before 2010
    mask_both = (temp_mask['term_end'] > '2010-01-01')
    #. Create a new dataframe = to the mask to temp_mask
    mask_offic = temp_mask.loc[mask_both]
    print('Count after 2010 filter')
    print(mask_offic.count())
    print(' ')
    print('Example:')
    print(mask_offic.head(2))

    leg_2010 = mask_offic
    return (leg_2010)


sources = [
    'https://theunitedstates.io/congress-legislators/legislators-current.json'
    , 'https://theunitedstates.io/congress-legislators/legislators-historical.json'
            ]


#. Pull from both sources!
cmbnd_results = pd.DataFrame()
for item in sources:
    print(item)
    cmbnd_results = cmbnd_results.append(leg_pull(item))
print(cmbnd_results.count())

#. We need to add some legislator term cycle information in to this dataframe. As in when the election cycle was.
cmbnd_results['cycle'] = cmbnd_results['term_start'].astype(str).str[:4].astype(int) - 1
print(cmbnd_results.head())


#. Let's print this info
final_results = cmbnd_results
final_results.to_csv(path_or_buf = 'C:\\Programming\\repos\\Open-secrets\\data\\leg_2010.csv')











    #? Useful tools from andrew
    # dict_keys(['webform', 'feccandid', 'cid', 'gender', 'comments', 'phone', 'office', 'party', 'exit_code'
    #, 'firstlast', 'bioguide_id', 'youtube_url', 'fax', 'facebook_id', 'website', 'lastname', 'birthdate'
    #, 'votesmart_id', 'first_elected', 'twitter_id', 'congress_office'])
    # print(columns)
    # print(type(columns))    # print(columns.keys())
    #     print(leg_data['firstlast'], leg_data['lastname'])
    #     # print(leg_data.keys())
    # columns = real_json_data[0]['@attributes']

    # csvfile = open('C:\\Programming\\repos\\Open-secrets\\test.csv', "w")
    # writer = csv.writer(csvfile, json_data['response']['legislator'].keys())
    # writer.writerows(json_data)
    # csvfile.close()


        # printer.pprint(json_data)
# printer.pprint(json_data.keys())
# printer.pprint(json_data['response'].keys())
# printer.pprint(json_data['response']['legislator'].keys())