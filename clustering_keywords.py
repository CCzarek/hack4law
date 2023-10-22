import ast
import copy

import numpy as np
import pandas as pd
import spacy
import seaborn as sns
from matplotlib import pyplot as plt
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# w tym pliku dzielimy na klastry czesc danych, mala czesc zeby przemielilo. zobaczymy jakie wyjda keywordy i polaczymy w klastry
# w tym pliku na sztywno wpisane jest 15 klastrow, mozna pokombinowac ale nie ma czasu chyba
# data puszczenia z n=430 i klastry=15: 6:50

df = pd.read_csv('preprocessed_2023.csv')

n=430
klastry = 15

df=df.head(n)

words=[]
paragrafy=[]
print(df['keywords'])

print(df.columns)


#df=df.head(100)
nokeys=0
noparas=0
for (idx, orzeczenie) in df.iterrows():
    if len(ast.literal_eval(orzeczenie['keywords']))==0:
        nokeys+=1
    if len(ast.literal_eval(orzeczenie['referencedRegulations_journalTitles']))==0:
        noparas+=1
    for word in ast.literal_eval(orzeczenie['keywords']):
        words.append(word)
    for par in ast.literal_eval(orzeczenie['referencedRegulations_journalTitles']):
        paragrafy.append(par)


print(len(set(words)))
print(noparas/len(df))

print(nokeys/len(df))

print(len(paragrafy))
print(len(set(paragrafy)))

# do tego momentu cos sobie tam sprawdzamy, nie ma tu nlp
df = df['textContent_notags']

df = df.dropna()

print(df)
#print(df.columns)

from nltk import sent_tokenize
from nltk import word_tokenize
from deep_translator import GoogleTranslator


def translate_text(text):
    # it requires texts to have max 5000 chars
    translator = GoogleTranslator(source='pl', target='en')
    max_len = 5000
    length = 0
    sentences = sent_tokenize(text)
    to_tranlate = ''
    translated = ''
    for sentence in sentences:
        if length + len(sentence) < max_len:
            to_tranlate += sentence
            length += len(sentence)
            continue
        if len(sentence) < max_len:
            translated += translator.translate(to_tranlate)
            to_tranlate = sentence
            length = len(sentence)
            continue
        # too big sentence
        length = 0
        words = word_tokenize(sentence)
        for word in words:
            if len(word) < max_len:
                translated += translator.translate(word)
            else:
                # strange words
                translated += word
    # the last translation
    if to_tranlate != '':
        translated += translator.translate(to_tranlate)

    return translated

def fun(x):
    try:
        return translate_text(x)
    except:
        return '-'

df = df.apply(lambda x: fun(x))

def simplify_text(text):
    try:
        vals = list([val.lower() for val in text if val.isalnum() or val == " "])
        return "".join(vals)
    except:
        return ("-")

df = df.apply(lambda x: simplify_text(x))


train_df, test_df = train_test_split(df, test_size=0.3, shuffle=False)

# extracting texts into variables
texts_train = copy.deepcopy(train_df)
texts_test = copy.deepcopy(test_df)


# tokenizing texts
texts_train_tokenized = [word_tokenize(text.lower()) for text in texts_train]
texts_test_tokenized = [word_tokenize(text.lower()) for text in texts_test]



# %% getting only alphabetic marks

alpha_texts_tokenized_train = [[word for word in text if word.isalpha()] for text in texts_train_tokenized]
alpha_texts_tokenized_test = [[word for word in text if word.isalpha()] for text in texts_test_tokenized]


texts_tokenized_without_stopwords_train = [[word for word in text if word not in stopwords.words('english')] for text in
                                           alpha_texts_tokenized_train]
texts_tokenized_without_stopwords_test = [[word for word in text if word not in stopwords.words('english')] for text in
                                          alpha_texts_tokenized_test]


nlp = spacy.load('en_core_web_sm')


def lemmatize_words(doc):
    doc = nlp(" ".join(doc))
    return [token.lemma_ for token in doc]


texts_lemmatized_spacy_train = list(map(lemmatize_words, texts_tokenized_without_stopwords_train))
texts_lemmatized_spacy_test = list(map(lemmatize_words, texts_tokenized_without_stopwords_test))


# %% tfidf vectorization

train_texts = [" ".join(text) for text in texts_lemmatized_spacy_train]
test_texts = [" ".join(text) for text in texts_lemmatized_spacy_test]

tfidf_vectorizer = TfidfVectorizer()

X_train_tfidf = tfidf_vectorizer.fit_transform(train_texts)

X_test_tfidf = tfidf_vectorizer.transform(test_texts)

# %% changing type of the result to data frame

X_train_tfidf_df = pd.DataFrame(X_train_tfidf.todense().A, columns=tfidf_vectorizer.get_feature_names_out())
X_test_tfidf_df = pd.DataFrame(X_test_tfidf.todense().A, columns=tfidf_vectorizer.get_feature_names_out())


def metrics_plots(X, max_k=10):
    score = []
    score_kmeans_s = []
    score_kmeans_c = []
    score_kmeans_d = []

    for k in range(2, max_k):
        kmeans = KMeans(n_clusters=k, random_state=101)
        predictions = kmeans.fit_predict(X)
        # Calculate cluster validation metrics and append to lists of metrics
        score.append(kmeans.score(X) * (-1))  # there was a mistake here before
        score_kmeans_s.append(silhouette_score(X, kmeans.labels_, metric='euclidean'))
        score_kmeans_c.append(calinski_harabasz_score(X, kmeans.labels_))
        score_kmeans_d.append(davies_bouldin_score(X, predictions))

    list_scores = [score, score_kmeans_s, score_kmeans_c, score_kmeans_d]
    # Elbow Method plot
    list_title = ['Within-cluster sum of squares', 'Silhouette Score', 'Calinski Harabasz', 'Davies Bouldin']
    for i in range(len(list_scores)):
        x_ticks = list(range(2, len(list_scores[i]) + 2))
        plt.plot(x_ticks, list_scores[i], 'bx-')
        plt.xlabel('k')
        plt.ylabel(list_title[i])
        plt.title('Optimal k')
        plt.show()

def plot_feature_importance(X, y, limit=10):
    # creating and fitting model
    decisionTreeClassifier = DecisionTreeClassifier(random_state=1)
    decisionTreeClassifier.fit(X, y)
    importance = decisionTreeClassifier.feature_importances_

    names = X.columns

    # creating arrays from feature importance and feature names
    feature_importance = np.array(importance)
    feature_names = np.array(names)

    # creating a DataFrame using a Dictionary
    data = {'feature_names': feature_names, 'feature_importance': feature_importance}
    fi_df = pd.DataFrame(data)

    # sorting the DataFrame in order decreasing feature importance
    fi_df.sort_values(by=['feature_importance'], ascending=False, inplace=True)

    # selecting a subset of features
    fi_df = fi_df.iloc[:limit]

    # defining size of bar plot
    plt.figure(figsize=(10, 8))
    sns.barplot(x=fi_df['feature_importance'], y=fi_df['feature_names'])
    plt.title('FEATURE IMPORTANCE')
    plt.xlabel('FEATURE IMPORTANCE')
    plt.ylabel('FEATURE NAMES')

#metrics_plots(X_train_tfidf_df)

n_clusters = klastry

kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init=10)

kmeans.fit(X_train_tfidf_df)

train_preds = kmeans.predict(X_train_tfidf_df)
test_preds = kmeans.predict(X_test_tfidf_df)


cluster_centers = kmeans.cluster_centers_

# we can add also a barplot to visualise devision
train_preds_summarized = pd.Series(train_preds).value_counts()
test_preds_summarized = pd.Series(test_preds).value_counts()

# %% feature importance

y = np.array(train_preds)
plot_feature_importance(X_train_tfidf_df, y, 10)


# %% draw barplot of cluster size - function

def plot_cluster_size_from_series(series, title):
    plt.bar(series.index, series.values)
    plt.xlabel('Nr klastra')
    plt.ylabel('Licznosc')
    plt.title(title)
    plt.show()


# %% KMeans - cluster sizes

plot_cluster_size_from_series(train_preds_summarized, 'Klastry KMeans zbior treningowy')
plot_cluster_size_from_series(test_preds_summarized, 'Klastry KMeans zbior testowy')


# similar results for train and test

# %% print cluster contents - function
#
# def print_cluster_contents(df, preds):
#     '''
#     for each cluster function summarizes how many of each directory end up inside
#
#     Parameters
#     ----------
#     df : pd.DataFrame
#         train_df, test_df or valid_df
#     preds : numpy.ndarray
#         the result of model prediction
#     '''
#     n = len(np.unique(preds))
#     directories = df['Directory']
#
#     for i in range(n):
#         print(f"CLUSTER NO. {i}")
#         indexes = np.where(preds == i)
#         directories_inside = directories.iloc[indexes]
#
#         for index, count in directories_inside.value_counts().head(3).items():
#             print(index, count)
#         print()


# %% some insight into result
# checking which directories end up in each cluster

# print_cluster_contents(train_df, train_preds)
# print_cluster_contents(test_df, test_preds)


# %% get top keywords from each cluster

cluster_labels = kmeans.labels_

print(cluster_labels)

f = open("lista_klastrow.csv", "w+")
for cluster in cluster_labels:
    f.write(str(cluster)+',')


data = test_texts

cluster_names = {}

for i in range(klastry):
    # Get the data points belonging to the current cluster
    cluster_data = [data[j] for j in range(len(data)) if cluster_labels[j] == i]

    # Extract keywords from the cluster data using TF-IDF
    tfidf_vector = tfidf_vectorizer.transform(cluster_data)
    feature_names = tfidf_vectorizer.get_feature_names_out()
    top_keywords = tfidf_vector.toarray().argsort()[:, ::-1][:, :50]  # Get top 3 keywords

    # Generate cluster name using top keywords
    cluster_name = ', '.join([feature_names[keyword_index] for keyword_index in top_keywords[0]])
    cluster_names[i] = cluster_name

for cluster_label, cluster_name in cluster_names.items():
    print(f"Cluster {cluster_label}: {cluster_name}")

