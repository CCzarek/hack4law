import numpy as np
import pandas as pd
import datetime
import ast
import re


pd.set_option('display.max_columns', None)
df = pd.read_csv('2023_orzeczenia.csv')

df['keywords'] = df['keywords'].apply(ast.literal_eval)

print(df.columns)
#print(df['decision'])
print(df.describe())

na_ratio_cols = df.isna().mean(axis=0)
print(na_ratio_cols)

df.info()

df.drop(columns=['Unnamed: 0', 'decision', 'receiptDate','meansOfAppeal', 'judgmentResult'], inplace=True)

df.info()

# summary ma 10% wartosci, a to sa te nie nany
df[df['summary'].notna()]['summary']
len(df[df['summary'].notna()]['summary'])

format = '%Y-%m-%d'

# convert from string format to datetime format

#print(datetime.datetime.strptime(df['judgmentDate'], format))
max_data=datetime.datetime.strptime('1970-01-01', format)
for (_, orzeczenie) in df.iterrows():
    tmp_data = datetime.datetime.strptime(orzeczenie['judgmentDate'], format)
    if tmp_data>max_data:
        max_data=tmp_data
#print(max(datatime(df['judgmentDate']))
print(max_data) # last date

# sprawdzanie czy dziala (czy bez duplikatow)
#print(sum(df.duplicated()))

# deleting data from 'future'
for (_, orzeczenie) in df.iterrows():
    if datetime.datetime.today() < datetime.datetime.strptime(orzeczenie['judgmentDate'], format):
        df.drop(_, inplace=True)


keywordsList = df['keywords'].tolist()
keywords = set()
for listk in keywordsList:
    for el in listk:
        keywords.add(el)
        

# cleaning textContent
CLEANR = re.compile('<.*?>')
def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  cleantext = re.sub(' +', ' ', cleantext)
  return cleantext.strip()

# function that gets list of jsons and returns list of values of one key
def jsonkey_converter(listOfJsonStrings, key):
    lista = ast.literal_eval(listOfJsonStrings)
    return [sub[str(key)] for sub in lista]


#print(df['textContent'][5839])
df['textContent_notags'] = df['textContent'].apply(lambda x: str(x).replace('\n', ' ').replace('\r', ''))
df['textContent_notags'] = df['textContent_notags'].apply(lambda x: cleanhtml(str(x)))


# deconstructing jsons to list of values from one key
df['courtCases'] = df['courtCases'].apply(lambda x: list(ast.literal_eval(x[1:-1]).values())[0])
df['division'] = df['division'].apply(lambda x: list(ast.literal_eval(x).values())[0])

df['referencedRegulations_journalTitles'] = df['referencedRegulations'].apply(lambda x: jsonkey_converter(x, 'journalTitle'))
df['referencedRegulations_texts'] = df['referencedRegulations'].apply(lambda x: jsonkey_converter(x, 'text'))

df['judges_names'] = df['judges'].apply(lambda x: jsonkey_converter(x, 'name'))

df['referencedCourtCases_caseNumbers'] = df['referencedCourtCases'].apply(lambda x: jsonkey_converter(x, 'caseNumber'))
df['referencedCourtCases_judgmentIds'] = df['referencedCourtCases'].apply(lambda x: jsonkey_converter(x, 'judgmentIds'))


#%% its dropping time
# TODO - think about what to drop and decide together

# all of them are []
# count=0
# for i in range(len(df)):
#     if len(ast.literal_eval(df['lowerCourtJudgments'][i]))>0:
#         count+=1
# print(count)

df.drop(columns=['judges', 'source', 'courtReporters', 'referencedRegulations', 'referencedCourtCases', 'lowerCourtJudgments'], inplace=True)

df.info()

df.replace(['None', 'nan'], np.nan, inplace=True)
df.fillna(' ', inplace=True)

## sth here ##
df.to_csv('preprocessed_2023.csv')

#%% 

# from deep_translator import GoogleTranslator

# translator = GoogleTranslator(source='pl', target='en')

#df['textContent_translated'] = df['textContent_notags'].apply(lambda x: translator.translate(x))


# from nltk import sent_tokenize
# from nltk import word_tokenize


#%% translating into en

# import nltk
# nltk.download('punkt')  # Download the Punkt tokenizer models
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
    

df['textContent_translated'] = df['textContent_notags'].apply(lambda x: translate_text(x))

def simplify_text(text):
    vals = list([val.lower() for val in text if val.isalnum() or val == " "])
    return "".join(vals)

df['textContent_translated'] = df['textContent_translated'].apply(lambda x: simplify_text(x))


df.to_csv('preprocessed_2023.csv')

