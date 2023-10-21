# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 19:51:49 2023

@author: Czarek
"""

import chromadb
from chromadb.config import Settings
import pandas as pd

df = pd.read_csv("preprocessed_2023.csv")

firstRow = df.iloc[0]
print(type(df['textContent'].to_list()[0]))


client = chromadb.PersistentClient(path="./path/to/chroma", settings=Settings(allow_reset=True))

client.reset()
textContent = client.create_collection("textContent_notags")
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
    documents=df['textContent_notags'].to_list(),
    ids=[str(i) for i in range(len(df['textContent'].to_list()))],
    metadatas=metadataList,
)

results = textContent.query(
    query_texts=["alimenty", "alkohol", "matka nie pozwala spotykać się z dzieckiem", "ma kiepskie samopoczucie"],
    n_results=2
)

print(results)


