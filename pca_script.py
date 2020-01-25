
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

pac_vote_totals_path = 'C:\\Programming\\repos\\Open-secrets\\data\\sum_pac_vote_data.csv'


#? We may need to come back to this, but for now, we need the label data as org_name
# pac_vote_totals = pd.read_csv(pac_vote_totals_path, index_col='org_name')
pac_vote_totals = pd.read_csv(pac_vote_totals_path)
#? I briefly took out these columns because I believed they were skewing the PCA, but it doesn't seems o
# pac_vote_totals = pac_vote_totals.drop(['indivs'], axis=1)
# pac_vote_totals = pac_vote_totals.drop(['pacs'], axis=1)
# pac_vote_totals = pac_vote_totals.drop(['total'], axis=1)
print(pac_vote_totals.shape)
#? For now we won't drop this, because PCA should drop it for us. It's redundant
# pac_vote_totals = pac_vote_totals.drop(['total'], axis=1)

#. We will split the data along labels and features though.
pac_numbers = pac_vote_totals.drop('org_name', 1)
pac_labels = pac_vote_totals['org_name']
print(pac_numbers.shape)
print(pac_labels.shape)

#. Let's split into train and test for numbers and labels
pac_numbers_train, pac_numbers_test, pac_labels_train, pac_labels_test = train_test_split(
    pac_numbers, pac_labels, test_size=0.2, random_state=0)

#. PCA requires normalized data, so we will do standard scalar normalization
sc = StandardScaler()
pac_numbers_train = sc.fit_transform(pac_numbers_train)
pac_numbers_test = sc.transform(pac_numbers_test)

#. PCA time
pca = PCA(n_components = 4)
pac_numbers_train= pca.fit_transform(pac_numbers_train)
pac_numbers_test = pca.transform(pac_numbers_test)

#. Results!
print(pca.explained_variance_ratio_)
print(pca.singular_values_)







#. Correlation matrix time

# # Compute the correlation matrix
# corr = pac_vote_totals.corr()

# # Generate a mask for the upper triangle
# mask = np.triu(np.ones_like(corr, dtype=np.bool))

# # Set up the matplotlib figure
# f, ax = plt.subplots(figsize=(11, 9))

# # Generate a custom diverging colormap
# cmap = sns.diverging_palette(220, 10, as_cmap=True)

# # Draw the heatmap with the mask and correct aspect ratio
# sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
#             square=True, linewidths=.5, cbar_kws={"shrink": .5})

# plt.show()









