#getLegislators pulls basic info for legislators by state

import urllib.request
import json
import pprint
import pandas as pd
import csv
#? Not sure what this does.
printer = pprint.PrettyPrinter(indent=4)


OS_API = '3f4cda9299c74fc3c21ff8e077a7a6e1'
state_List = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA'
    , 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD'
    , 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ'
    , 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC'
    , 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
    ]

def OS_Search(item):
    api_key = OS_API
    url_Base = 'https://www.opensecrets.org/api/?method=getLegislators'
# state = 'NJ'
    state = item
    output = 'json'
    final_url = url_Base + "&id=" + state + "&apikey=" + api_key + '&output=' + output

    #. Pretend to be Mozilla. This might need to be updated.
    #. Make a variable for the request when a specific url.
    req = urllib.request.Request(final_url, headers={'User-Agent': 'Mozilla/5.0'})

    #. Open this variable and assign it to a new variable
    return_value = urllib.request.urlopen(req)

    #. Gives us a status code for how the pull went
    print(return_value.status)
    body = return_value.read()

    #. Decode to utf-8 by default
    #! Worked before, could cause problems this time
    decoded_body = body.decode('utf-8')
    json_data = json.loads(decoded_body)

    #. Ok. Let's get these legislators into a dataframe
    legislators = pd.DataFrame()
    incr = 0
    #. Carve down to each legislator themselves
    real_json_data = json_data['response']['legislator']
    #. Turn each row into a dataframe and append them together
    for data_point in real_json_data:
        leg_data = data_point['@attributes']
        leg_data_pd = pd.DataFrame(leg_data, index = [incr])
        legislators = legislators.append(leg_data_pd)
        incr +=1
    return (legislators)

#     #. Let's print this info
#     legislators.to_csv(path_or_buf = 'C:\\Programming\\repos\\Open-secrets\\legislators.csv')

# OS_Search('DE')
# exit()




#. OS_Search(state_List)
all_Data = pd.DataFrame()
for item in state_List:
    print(item)
    all_Data = all_Data.append(OS_Search(item))

#. Let's print this info
all_Data.to_csv(path_or_buf = 'C:\\Programming\\repos\\Open-secrets\\legislators.csv')











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