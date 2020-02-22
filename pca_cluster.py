

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import scale

import sklearn.metrics as sum_pac_vote_data
from sklearn import datasets
from sklearn.metrics import confusion_matrix, classification_report

#> Now that all of our data is together, we run PCA and clustering algorithms on the result of vv_votes_2_PACs.py

#. Let's oepn our main data file
pac_vote_totals_path = 'C:\\Coding\\repos\\pac_categories\\data\\sum_pac_vote_data.csv'


#? We may need to come back to this, but for now, we need the label data as org_name
#// pac_vote_totals = pd.read_csv(pac_vote_totals_path, index_col='org_name')
pac_vote_totals = pd.read_csv(pac_vote_totals_path)
#! We are dropping these columns for now as they carry magnitude while the bill counts do not.
pac_vote_totals = pac_vote_totals.drop(['indivs'], axis=1)
pac_vote_totals = pac_vote_totals.drop(['pacs'], axis=1)
pac_vote_totals = pac_vote_totals.drop(['total'], axis=1)
print(pac_vote_totals.shape)


#. We will split the data along labels and features.
pac_numbers = pac_vote_totals.drop('org_name', 1)
pac_labels = pac_vote_totals['org_name']
print("PAC Numbers' Shape:", pac_numbers.shape)
print("PAC Labels' Shape:", pac_labels.shape)

#. Let's split into train and test for numbers and labels
X_train, X_test, pac_names_train, pac_names_test = train_test_split(
    pac_numbers, pac_labels, test_size=0.2, random_state=1)

#> Begin setting up PCA so that
#. PCA requires normalized data, so we will do standard scalar normalization
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

#. PCA time
pca = PCA(n_components = 4)
X_train= pca.fit_transform(X_train)
X_test = pca.transform(X_test)

#. Results!
print('Explained variance of each compoent/dimension:', pca.explained_variance_ratio_)
# print(pca.singular_values_)


#> Figure out how many clusters we need. I settled on 9 here through use of a distortion
#> graph made using the elbow method. Measuring how far away each point is from its centroid.
inertia = []
for i in range(1, 15):
    km = KMeans(
        n_clusters=i, init='random',
        n_init=10, max_iter=300,
        tol=1e-04, random_state=0
    )
    km.fit(X_train)
    inertia.append(km.inertia_)
print('Cluster Inertia:', inertia)

#. plot them out for analysis
plt.plot(range(1, 15), inertia, marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
#? If you want to print the Elbow Method:
# plt.show()


#> Start building the kmeans model!
km = KMeans(
    n_clusters=9, init='random',
    n_init=10, max_iter=300,
    tol=1e-04, random_state=0
)

#. Fit the model and fit_predict the test data
km_fit = km.fit(X_train)
clusters = km.fit_predict(X_test)

#? For reference
# print(clusters)
# print(pac_names_test)

#. Identify the centroids and print for reference
centroids = km.cluster_centers_
print(centroids)

#. Align the clusters to each Pac Name for further analysis
cluster_pac_list = []
for x, y in zip(clusters, pac_names_test):
    cluster_pac_list.append([x, y])

#. Transfer to a dataframe for legibility
cluster_pac_pd = pd.DataFrame(cluster_pac_list, columns=['Cluster', 'PAC Name'])

#. Print the cluster group counts for reference
grouped_pd = cluster_pac_pd.groupby('Cluster').count()
print(grouped_pd)















#? Consider using a correlation matrix
# Correlation matrix time

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


