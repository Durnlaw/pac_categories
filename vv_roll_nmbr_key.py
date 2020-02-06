
#> This program is used to combine all >2010 House/Senate bills into one csv from bulk data. Specifically
#> targets bills requiring presidential signature. Includes a key to identify the bill by Chamber,
#> Congress, and rollnumber. The output is used for pivoting later.

import pandas as pd
import numpy as np
import os

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


def roll_nmbr_key(cycle):
    #. Call in each rollcall file
    roll_call_file = 'C:\\Programming\\data\\Open-secrets\\vote_view\\%s\\HS%s_rollcalls.csv' % (cycle, cycle)
    roll_calls = pd.read_csv(roll_call_file)

    #. Determine how many rows there are in the file
    print('true start:', roll_calls.count())

    #. Replace any blank bill numbers with a "holder" that will be used to drop those rows later
    roll_calls['bill_number'].replace(np.nan, 'holder', inplace = True)

    #. We care about all other bill types except these below.
    drop_list = ['HCONRES', 'SCONRES', 'HRES', 'SRE', 'holder']

    #. This drops the bill types and reports how many were dropped.
    print(' ')
    print('------------------------------------------------------')
    for typ in drop_list:
            start = roll_calls['bill_number'].count()
            roll_calls = roll_calls[~roll_calls.bill_number.str.contains(typ, na=False)]
            end = roll_calls['bill_number'].count()
            print(typ, 'count of rows dropped', start-end)



    #> Ok now we make a key to be used as a pivot later on. This will tie to the votes dataset later as a key.
    #. It is made of chamber, cycle, and bill number.

    roll_calls['house_cyc_roll'] = roll_calls['chamber'] + '_' + roll_calls['congress'].map(str) + '_' + roll_calls['rollnumber'].map(str)
    roll_calls['house_cyc_roll_bill'] = roll_calls['chamber'] + '_' + roll_calls['congress'].map(str) + '_' + roll_calls['rollnumber'].map(str) + '_' + roll_calls['bill_number']
    print(' ')
    print('------------------------------------------------------')
    print("Column created correctly?")
    print(roll_calls['house_cyc_roll_bill'].head(1))

    #. Dedup check. This key should be unique. Or we hope it is.
    print(' ')
    print('------------------------------------------------------')
    print('Non-deduped count: ', roll_calls['house_cyc_roll_bill'].count())
    roll_calls['house_cyc_roll_bill'].drop_duplicates(keep = 'first')
    print('deduped count', roll_calls['house_cyc_roll_bill'].count())

    print(' ')
    print('------------------------------------------------------')

    roll_calls_unique = roll_calls[['house_cyc_roll', 'house_cyc_roll_bill', 'bill_number']]
    return roll_calls_unique


#> Run through each year that we have on file now.
file = [113,114, 115, 116]

#. Append them all together and print it out as a csv for later use.
key_list = []
for x in file:
    print('Cycle: ', x)
    print('====================================================================================')
    print(' ')
    key_list.append(roll_nmbr_key(x))
    # print(key_list.count())

unique_keys = pd.concat(key_list)
print(unique_keys.count())

#. Nice job. Print this sucker.
unique_keys.to_csv(
    path_or_buf = 'C:\\Programming\\repos\\Open-secrets\\data\\vv_house_cyc_roll_bill_ids.csv',
    header = 'house_cyc_roll_bill')

