

import urllib.request
import json
import pprint
import pandas as pd
import csv
import time
#? Not sure what this does.
printer = pprint.PrettyPrinter(indent=4)


OS_API = '3f4cda9299c74fc3c21ff8e077a7a6e1'

def OS_donations(cand, cycle):
    api_key = OS_API
    url_Base = 'https://www.opensecrets.org/api/?method=candContrib'
    output = 'json'
    final_url = url_Base + "&cid=" + cand + "&cycle=" + cycle + "&apikey=" + api_key + '&output=' + output
    print(final_url)

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
    leg_don_pd['cycle'] = cycle
    print(cand, cycle, "Done")
    return(leg_don_pd)


leg_data = pd.read_csv(filepath_or_buffer  = 'C:\\Programming\\repos\\Open-secrets\\data\\leg_2010.csv')

leg_id = leg_data['opensecrets'].values.tolist()
cycle_id = leg_data['cycle'].astype(str).values.tolist()

print("leg id count: ", len(leg_id))
print("cycle id count: ", len( cycle_id))



# leg_id = ['N00007360', 'N00007360', 'N00007360']
# cycle_id = ['2020', '2018', '2016']

#> Ok we have to set up the actual loops that call the API now. The overall goal is to get our program to call
#> the full 200 limit each day, but avoid problems we have with getting kicked out of the API early. 
#> So we have some if criteria to write to a csv intermittently, so that if we get kicked we don't lose much.

#. Set the limits of starting and ending
start_row = 1032
end_row = 1232

#. Set the limits to be used in the for loop
test_iter = start_row - 1
test_end = end_row - 1

#. Set up a dataframe for storage
final_donations = pd.DataFrame()



#. For each row in the leg_2010 file
for polit_cycle in leg_id:

    #. First if logic. If it's test_iter = end_row. Then break.
    if test_iter == end_row:
        print('We stop here now. Start here next time. Use as commit marker.')
        print(leg_id[test_iter],cycle_id[test_iter])
        break

    #. If it's the first run, we don't want it printing a csv of one. This means if we
    #. start on a # divisible by 5, then the next csv pushed will be 6 rows long.
    if test_iter == start_row - 1:
        print('start')
        print(leg_id[test_iter],cycle_id[test_iter])
        final_donations = final_donations.append(
                                OS_donations(leg_id[test_iter], cycle_id[test_iter]))
        time.sleep(10)
        test_iter+=1

    #. This part will push a csv any time it is divisible by 5
    elif test_iter%5 == 0:
        print('Excel else')
        print(leg_id[test_iter],cycle_id[test_iter])
        final_donations = final_donations.append(
                                OS_donations(leg_id[test_iter], cycle_id[test_iter]))
        path = 'C:\\Programming\\repos\\Open-secrets\\data\\os_pac\\{0}.csv'.format(test_iter)
        final_donations.to_csv(path_or_buf = path)
        time.sleep(10)
        test_iter+=1
        #. Blank the dataframe so it's clean for next run
        final_donations = pd.DataFrame()

    #. Now let's print the last group following a 5 that don't end in a 5 modulo.
    elif test_iter == end_row - 1:
        print('End')
        print(leg_id[test_iter],cycle_id[test_iter])
        final_donations = final_donations.append(
                                OS_donations(leg_id[test_iter], cycle_id[test_iter]))
        path = 'C:\\Programming\\repos\\Open-secrets\\data\\os_pac\\{0}.csv'.format(test_iter)
        final_donations.to_csv(path_or_buf = path)
        time.sleep(10)
        test_iter+=1
        #. Blank the dataframe so it's clean for next run
        final_donations = pd.DataFrame()

    #. Last one will simply add to final_donations each time it isn't divisible by 5
    elif test_iter%5 != 0:
        print('Not Excel')
        print(leg_id[test_iter],cycle_id[test_iter])
        final_donations = final_donations.append(
                                OS_donations(leg_id[test_iter], cycle_id[test_iter]))
        time.sleep(10)
        test_iter+=1
























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