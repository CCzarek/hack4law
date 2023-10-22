# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 19:51:49 2023

@author: Czarek
"""

import chromadb
from chromadb.config import Settings
import pandas as pd
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
        length = 0
        words = word_tokenize(sentence)
        for word in words:
            if len(word) < max_len:
                translated += translator.translate(word)
            else:
                # strange words
                translated += word
    if to_tranlate != '':
        translated += translator.translate(to_tranlate)
    
    return translated

df = pd.read_csv("preprocessed_2023_100.csv")
df.rename(columns={"Unnamed: 0": "index"})

firstRow = df.iloc[0]

def search(content, text, quantity = 5):
    translatedText = translate_text(text)
    results = content.query(
        query_texts=text,
        n_results=quantity
        )
    return results['ids'][0]

def main():  
    client = chromadb.HttpClient(host='localhost', port=8000)
    #client.reset()
    textContent = client.get_collection("textContent_notags_eng100")
    [str(i) for i in range(len(df['textContent'].to_list()))]
    
    
    metadata = ['courtType', 'judgmentType']
    metadataList = []
    for index, row in df.iterrows():
        row_dict = {k: row[k] for k in metadata}
        metadataList.append(row_dict)
    
    
    textContent.add(
        documents=df['textContent_translated'].to_list(),
        ids=[str(i) for i in df['index'].to_list()],
        metadatas=metadataList,
    )

if __name__ == "__main__":
    main()
