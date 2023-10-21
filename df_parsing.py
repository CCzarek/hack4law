import pandas as pd
import datetime

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


format = '%Y-%m-%d'
input = '2021/05/25'

# convert from string format to datetime format

#print(datetime.datetime.strptime(df['judgmentDate'], format))
max_data=datetime.datetime.strptime('1970-01-01', format)
for (_, orzeczenie) in df.iterrows():
    tmp_data = datetime.datetime.strptime(orzeczenie['judgmentDate'], format)
    if tmp_data>max_data:
        max_data=tmp_data
#print(max(datatime(df['judgmentDate']))
print(max_data)

# sprawdzanie czy dziala (czy bez duplikatow)
print(df.duplicated())

print(sum(df.duplicated()))

print(df.iloc[0]==df.iloc[100])

print(df['summary'].values[100], print(df['summary'].values[200]))