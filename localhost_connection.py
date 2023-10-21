# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 01:13:07 2023

@author: biuro
"""

import chromadb
chroma_client = chromadb.HttpClient(host='localhost', port=8000)

chroma_client.list_collections()

collection = chroma_client.get_collection("textContent_notags")

results = collection.query(
    query_texts=["alimenty", "alkohol", "matka nie pozwala spotykać się z dzieckiem", "ma kiepskie samopoczucie"],
    n_results=2
)

results
