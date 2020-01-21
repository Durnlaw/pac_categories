import pandas as pd
import numpy as np
import os

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


def vote_pvt(cycle):
    #. Call in each vote file
    vote_file = 'C:\\Programming\\data\\Open-secrets\\vote_view\\%s\\HS%s_votes.csv' % (cycle, cycle)
    votes = pd.read_csv(vote_file)

    #. Determine how many rows there are in the file
    print('Votes in cycle:', votes.count())

    #. Let's make all Yea's a "1", all others a "0" for the purpose of the model we are aiming for.
    #? This won't accomadate for all of the other styles of "Yea" votes that are possible but unseen in this data (Namely 2 and 3)
    print('Types of votes:', votes.cast_code.unique())
    votes['cast_code'].replace(to_replace = [2,3,4,5,6,7,8,9], value = 0, inplace = True)

    #. Let's make the key that will be pivoted up
    votes['house_cyc_roll_bill'] = votes['chamber'] + '_' + votes['congress'].map(str) + '_' + votes['rollnumber'].map(str)

    #. Make a table for pivoting
    pvt_prep = votes[['house_cyc_roll_bill', 'icpsr', 'cast_code']]
    print (pvt_prep.head())

    #. Get pivoting!
    pvt = pvt_prep.pivot(index='icpsr', columns = 'house_cyc_roll_bill', values= 'cast_code')
    print(pvt.iloc[0:2, 0:5])
    print('Cycle', cycle, 'shape:', pvt.shape)

    return pvt


file = [113,114, 115, 116]

#. Append them all together and print it out as a csv for later use.
votes_list = []
for x in file:
    print('Cycle: ', x)
    print('====================================================================================')
    print(' ')
    votes_list.append(vote_pvt(x))
    # print(key_list.count())

votes_as_columns = pd.concat(votes_list, axis = 1)
# , ignore_index = True, sort=False
print('Final shape:',votes_as_columns.shape)
# print(votes_as_columns['icpsr'].unique().count())


#! This thing is too large to really print to a csv usefully, so we are starting the next step of the proj in this same program
#. Nice job. Print this sucker.
# votes_as_columns.to_csv(
#     path_or_buf = 'C:\\Programming\\repos\\Open-secrets\\data\\vv_votes_cols.csv')