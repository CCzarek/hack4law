# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 16:45:19 2023

@author: biuro
"""


import spacy

# in english
nlp = spacy.load('en_core_web_md')

dog = nlp("dog")
dog.vector

cat = nlp("cat")
cat.vector

dig = nlp("dig")
dig.vector

dog.similarity(cat)
cat.similarity(dog)

dig.similarity(cat)


# in polish
nlp = spacy.load('pl_core_news_sm')

dog = nlp("pies")
dog.vector

cat = nlp("kot")
cat.vector

dog2 = nlp("owczarek niemiecki")
dog2.vector

dog.similarity(cat)
cat.similarity(dog)

dog2.similarity(cat)
dog2.similarity(dog)
