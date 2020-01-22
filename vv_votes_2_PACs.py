import pandas as pd
import numpy as np
import io
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


#> Run the function for each cycle of congress
file = [113,114, 115, 116]

votes_list = []
for x in file:
    print('Cycle: ', x)
    print('====================================================================================')
    print(' ')
    votes_list.append(vote_pvt(x))

#. Concat them all together and ensure all columns align to ICPSR as the index.
votes_as_columns = pd.concat(votes_list, axis = 1)
print('Final shape:',votes_as_columns.shape)

#! This thing is too large to really print to a csv usefully, so we are starting the next step of the proj in this same program
#. Nice job. Print this sucker.
# votes_as_columns.to_csv(
#     path_or_buf = 'C:\\Programming\\repos\\Open-secrets\\data\\vv_votes_cols.csv')


#> Now let's pull in leg_2010.csv. This will give us a list of all unique congresspeople, icpsr's, and opensecrets ids
leg_2010_path = 'C:\\Programming\\repos\\Open-secrets\\data\\leg_2010.csv'
leg_2010_key = pd.read_csv(leg_2010_path)
leg_2010_key = leg_2010_key[['first', 'last', 'first_last', 'bioguide', 'icpsr', 'opensecrets']].drop_duplicates()
print('Legislator dedup shape', leg_2010_key.shape)


#> Time to pull in every OS_pac file we have.
os_pac_list = []
os_pac_path = 'C:\\Programming\\repos\\Open-secrets\\data\\os_pac\\'
for filename in os.listdir(os_pac_path):
    # t = '{}'.format(filename).encode('utf-8').decode('utf-8')
    print(filename)
    os_pac_file = pd.read_csv(os_pac_path+filename)

    #. Select only needed rows
    os_pac_data = os_pac_file[['org_name', 'indivs', 'pacs', 'total', 'cid']]
    os_pac_list.append(os_pac_data)

#. Concat them together
pac_data = pd.concat(os_pac_list)
print('PAC data shape:', pac_data.shape)

#. Let's try to group the data up to reduce duplicates and preserve the $$. Index to false to preserve the grouped columns
grouped_pac_data = pac_data.groupby(['org_name', 'cid'], as_index=False)[['indivs', 'pacs', 'total']].sum()
print('PAC data shape:', grouped_pac_data.shape)
print(grouped_pac_data.head(5))



#. Alright, now we need to merge the other id's and names of each congressperson to the grouped_pac_data
grouped_pac_cand_data = pd.merge(grouped_pac_data, leg_2010_key, left_on='cid', right_on='opensecrets')
print('PAC data and congresspeople shape:', grouped_pac_cand_data.shape)
print(grouped_pac_cand_data.head(5))



#. Ok. Now let's get the vote data (in all it's glory) and attach it to the right of a trimmed grouped_pac_cand_data
grouped_pac_cand_vote_data = pd.merge(grouped_pac_cand_data, votes_as_columns, on='icpsr')
grouped_pac_vote_data = grouped_pac_cand_vote_data.drop(['cid', 'first', 'last', 'first_last', 'bioguide', 'icpsr', 'opensecrets'],
                                                        axis = 1)
print('PAC data and votes shape:', grouped_pac_vote_data.shape)

#. Now we sum based on org_name and have all of paid votes by bill by each PAC. 
sum_pac_vote_data = grouped_pac_vote_data.groupby(['org_name'], as_index=False).sum()
print(sum_pac_vote_data.shape)

#. Let's confirm that the max is not ridiculously low or high.
temp = sum_pac_vote_data.drop(['org_name', 'indivs', 'pacs', 'total'], axis = 1)
maxValue = temp[:].max()
print(maxValue.head(5))
print(maxValue.max())


#> Data file done! Let's try to print to a csv then reopen to see if everything is preserved. Not sure if it will be
print(sum_pac_vote_data.iloc[:, 11:].sum().sum())
sum_pac_vote_data.to_csv(
    path_or_buf = 'C:\\Programming\\repos\\Open-secrets\\data\\sum_pac_vote_data.csv')

#! When I reopen this file, it adds an index (extra column).
test_path = 'C:\\Programming\\repos\\Open-secrets\\data\\sum_pac_vote_data.csv'
test_file = pd.read_csv(test_path)
#. We move the iloc out one column to account for the index column that gets added.
print(test_file.iloc[:, 12:].sum().sum())
print(test_file.shape)


