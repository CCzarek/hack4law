# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 19:51:49 2023

@author: Czarek
"""

import chromadb
from chromadb.config import Settings
import pandas as pd
from df_parsing import translate_text

df = pd.read_csv("preprocessed_2023_100.csv")

firstRow = df.iloc[0]


client = chromadb.HttpClient(host='localhost', port=8000)
#client.reset()
textContent = client.get_collection("textContent_notags_eng100")
[str(i) for i in range(len(df['textContent'].to_list()))]


metadata = ['courtType', 'judgmentType']
metadataList = []
for index, row in df.iterrows():
    row_dict = {k: row[k] for k in metadata}
    metadataList.append(row_dict)


count=0
for i in range(4565):
    if type(df['textContent_notags'].to_list()[i])!=str:
        print(i)
        count+=1
count

textContent.add(
    documents=df['textContent_translated'].to_list(),
    ids=[str(i) for i in range(len(df['textContent'].to_list()))],
    metadatas=metadataList,
)
 
def search(content ,text, quantity = 5):
    translatedText = translate_text(text)
    results = content.query(
        query_texts=text,
        n_results=quantity
        )
    return results['ids'][0]

