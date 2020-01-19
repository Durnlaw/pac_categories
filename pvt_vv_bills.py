
import pandas as pd
import numpy as np
import os

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


def bill_pvt(cycle):
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

    roll_calls['house_cyc_bill_roll'] = roll_calls['chamber'] + '_' + roll_calls['congress'].map(str) + '_' + roll_calls['bill_number'] + '_' + roll_calls['rollnumber'].map(str)
    print(' ')
    print('------------------------------------------------------')
    print("Column created correctly?")
    print(roll_calls['house_cyc_bill_roll'].head(1))

    #. Dedup check. This key should be unique. Or we hope it is.
    print(' ')
    print('------------------------------------------------------')
    print('Non-deduped count: ', roll_calls['house_cyc_bill_roll'].count())
    roll_calls['house_cyc_bill_roll'].drop_duplicates(keep = 'first')
    print('deduped count', roll_calls['house_cyc_bill_roll'].count())

    print(' ')
    print('------------------------------------------------------')

    roll_calls_unique = roll_calls['house_cyc_bill_roll']
    return roll_calls_unique


file = [113
        ,114, 115, 116
        ]

key_list = []
for x in file:
    print('Cycle: ', x)
    print('=========================================================================')
    print(' ')
    key_list = key_list.append(bill_pvt(x))

unique_keys = pd.concat(key_list)
print(unique_keys.count())

