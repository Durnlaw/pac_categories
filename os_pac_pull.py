

import urllib.request
import json
import pprint
import pandas as pd
import csv
#? Not sure what this does.
printer = pprint.PrettyPrinter(indent=4)


OS_API = '3f4cda9299c74fc3c21ff8e077a7a6e1'

def OS_donations(cand, cycle):
    api_key = OS_API
    url_Base = 'https://www.opensecrets.org/api/?method=candContrib'
    output = 'json'
    final_url = url_Base + "&cid=" + cand + "&cycle=" + cycle + "&apikey=" + api_key + '&output=' + output

    #. Pretend to be Mozilla. This might need to be updated.
    #. Make a variable for the request when a specific url.
    req = urllib.request.Request(final_url, headers={'User-Agent': 'Mozilla/5.0'})

    #. Open this variable and assign it to a new variable
    return_value = urllib.request.urlopen(req)

    #. Gives us a status code for how the pull went
    print(return_value.status)
    body = return_value.read()

    #. Decode to utf-8 by default
    decoded_body = body.decode('utf-8')
    json_data = json.loads(decoded_body)

    #. Let's drill into the canididate information
    cand_json_data = json_data['response']['contributors']['@attributes']
    my_dict = {}
    my_dict['cand_name']=cand_json_data.get('cand_name')
    my_dict['cid']=cand_json_data.get('cid')
    print(my_dict)

    #. Holder for all legislator donations
    leg_donations = []

    #. Now that we have the cand info, let's tack on the PAC information
    contrib_json_data = json_data['response']['contributors']['contributor']
    iter = 0
    for y in contrib_json_data:
        my_dict2 = {}
        #. Bring the cand info forward
        my_dict2['cand_name'] = my_dict['cand_name']
        my_dict2['cid'] = my_dict['cid']

        #. Call the new information and add it next to the candidate info
        my_dict2['total'] = contrib_json_data[iter].get('@attributes').get('total')
        my_dict2['org_name'] = contrib_json_data[iter].get('@attributes').get('org_name')
        my_dict2['pacs'] = contrib_json_data[iter].get('@attributes').get('pacs')
        my_dict2['indivs'] = contrib_json_data[iter].get('@attributes').get('indivs')
        iter+=1
        #. Append all info to the same list
        leg_donations.append(my_dict2)

    #. Turn it into a dataframe
    leg_don_pd = pd.DataFrame(leg_donations)
    print(leg_don_pd)



#     #. Let's print this info
#     legislators.to_csv(path_or_buf = 'C:\\Programming\\repos\\Open-secrets\\legislators.csv')

    # return (legislators)


OS_donations('N00007360', '2020')
# exit()




# #. OS_Search(state_List)
# all_Data = pd.DataFrame()
# for item in state_List:
#     print(item)
#     all_Data = all_Data.append(OS_Search(item))

# #. Let's print this info
# all_Data.to_csv(path_or_buf = 'C:\\Programming\\repos\\Open-secrets\\legislators.csv')











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