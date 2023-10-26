import ast
from statistics import mode

import pandas as pd

# w tym pliku chcemy uzupelnic brakujace w dfce keywordy na podstawie podzialu na klastry i/lub slow kluczowych w klastrach

f=open("lista_klastrow.csv", "r+")

for line in f.readlines():
    clusters = (list(ast.literal_eval(line)))


df = pd.read_csv('preprocessed_2023.csv')
df = df.head(len(clusters))

n_clusters = max(clusters)+1

print(n_clusters)
print(len(df))

i=0
df['cluster'] = pd.Series(clusters)

print(df['cluster'])



print(n_clusters)
keywords_clusters = [[] for _ in range(n_clusters)]
print(keywords_clusters)

for i in range(301):
    tmp_clus = df.loc[i, 'cluster']
    tmp_keywords = list(ast.literal_eval(df.loc[i, 'keywords']))
    for keyword in tmp_keywords:
        keywords_clusters[tmp_clus].append(keyword)

    #(keywords_clusters[tmp_clus]).extend(tmp_keywords)

#print(keywords_clusters)

from collections import Counter

def most_common_elements(lst, n):
    # Use Counter to count the occurrences of each element
    counts = Counter(lst)

    # Get the n most common elements and their counts
    common_elements = [element for element, _ in counts.most_common(n)]

    return common_elements

to_fill = []
for i in range(n_clusters):
    to_fill.append(most_common_elements(keywords_clusters[i], 3))

print(to_fill)

df = pd.read_csv('preprocessed_2023.csv')
df = df.head(len(clusters))
df['cluster'] = pd.Series(clusters)


def new_column(row):
    return to_fill[(row['cluster'])]

# Apply the function to each row and create a new column 'new_column'
df['cluster_keywords'] = df.apply(new_column, axis=1)


print(df['cluster_keywords'])

df.to_csv('301_processed_with_clustering.csv')
