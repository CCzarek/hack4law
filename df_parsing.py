import pandas as pd

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

print((df['judgmentDate']))