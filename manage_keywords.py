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
i=0
df['cluster'] = pd.Series(clusters)

#print(df['cluster'])

#print(n_clusters)
keywords_clusters=[list()]*n_clusters
#print(keywords_clusters)

# TODO - mamy liste z okolo 300 (na razie 21) dopasowaniami do klastrow. teraz dzieki temu mozemy w jakis sposob dodac
# TODO - do klastra w polu 'keywords' brakuj¹ce keywordy - pewnie na podstawie mody z keywordow z tego samego klastra

# tu nieudolne proby przemeczonego czlowieka
for (idx, orzeczenie) in df.iterrows():
    print(orzeczenie['cluster'])
    for keyword in ast.literal_eval(orzeczenie['keywords']):
        print(keyword)
        keywords_clusters[int(orzeczenie['cluster'])].append(keyword)
    #keywords_clusters[int(orzeczenie['cluster'])].extend(list(ast.literal_eval(orzeczenie['keywords'])))

print(keywords_clusters[0])
print(keywords_clusters[1])
print(keywords_clusters[2])

for i in range(len(keywords_clusters)):
    print(mode(keywords_clusters[i]))
#print(df.loc[:,"cluster"])

