import pandas as pd
import datetime
import re


pd.set_option('display.max_columns', None)
df = pd.read_csv('2023_orzeczenia.csv')

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
print(sum(df.duplicated()))

# deleting data from 'future'
for (_, orzeczenie) in df.iterrows():
    if datetime.datetime.today() < datetime.datetime.strptime(orzeczenie['judgmentDate'], format):
        df.drop(_, inplace=True)


# cleaning textContent
CLEANR = re.compile('<.*?>')
def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)

  return cleantext.strip()

#print(df['textContent'][5839])
df['textContent'] = df['textContent'].apply(lambda x: cleanhtml(str(x)))
df['textContent'] = df['textContent'].apply(lambda x: x.replace('\n', ' ').replace('\r', ''))

print(df['textContent'])
