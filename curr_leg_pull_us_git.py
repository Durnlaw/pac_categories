#getLegislators pulls basic info for legislators by state

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
    #! Worked before, could cause problems this time
    # decoded_body = body.loads(body.decode('utf-8'))

    decoded_body = body.decode('utf-8')
    # print(decoded_body)
    decoded_body = json.loads(decoded_body)
    # print(type(decoded_body))

    results = []
    for x in decoded_body:
        my_dict = {}
        my_dict['bioguide']=x.get('id').get('bioguide')
        my_dict['opensecrets']=x.get('id').get('opensecrets')
        my_dict['icpsr']=x.get('id').get('icpsr')
        my_dict['first']=x.get('name').get('first')
        my_dict['last']=x.get('name').get('last')
        my_dict['first_last']=x.get('name').get('official_full')
        my_dict['term_start']=x.get('terms')[0].get('start')
        my_dict['term_end']=x.get('terms')[0].get('end')
        # print(my_dict.head(2))
        results.append(my_dict)

    print('Count: ', len(results))
    print('--------------------------------------')
    print('Example:')
    print(results[:1])
    print(' ')
    print(' ')

    # return (results)
    #. Let's print this info
    test = pd.DataFrame(results)
    test.to_csv(path_or_buf = 'C:\\Programming\\repos\\Open-secrets\\test.csv')


sources = [
    'https://theunitedstates.io/congress-legislators/legislators-current.json'
            # , 'https://theunitedstates.io/congress-legislators/legislators-historical.json'
            ]


#. Pull from both sources!
all_leg = pd.DataFrame()
for item in sources:
    print(item)
    all_leg = all_leg.append(leg_pull(item))
print(all_leg.head(2))

#. No dupes found. Drop all congresspeople that started before 2010
all_leg['term_end'] = pd.to_datetime(all_leg['term_end'])

mask = (all_leg['term_end'] > '2010-01-01')
leg_2010 = all_leg.loc[mask]
print(leg_2010.count())
print(leg_2010.head(2))

#. Let's print this info
leg_2010.to_csv(path_or_buf = 'C:\\Programming\\repos\\Open-secrets\\leg_2010.csv')











    #? Useful tools from andrew
    # dict_keys(['webform', 'feccandid', 'cid', 'gender', 'comments', 'phone', 'office', 'party', 'exit_code'
    #, 'firstlast', 'bioguide_id', 'youtube_url', 'fax', 'facebook_id', 'website', 'lastname', 'birthdate'
    #, 'votesmart_id', 'first_elected', 'twitter_id', 'congress_office'])
    # print(columns)
    # print(type(columns))
    # print(columns.keys())
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