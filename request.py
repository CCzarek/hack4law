# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 10:47:53 2023

@author: biuro
"""

# pip install requests

import requests

# %% data dowload functions

def get_data(api_url, params=None):
    try:
        if params == None:
            response = requests.get(api_url)
        else:
            response = requests.get(api_url, params = params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def req(pages):
    data = []
    for i in range(pages):
        url = "https://www.saos.org.pl/api/dump/judgments?pageSize=100&judgmentStartDate=2022-01-01" + "&pageNumber=" + str(i)
        data_add = get_data(url)["items"]
        if data_add != None:
            data += get_data(url)["items"]
    return data


def get_data_pages(pages, url, params=None):
    data = []
    base_url = url
    for i in range(pages):
        tmp_url = base_url + "&pageNumber=" + str(i)
        data_add = get_data(tmp_url, params)["items"]
        if data_add != None:
            data += data_add
    return data



# %% loading all decisions from one year

page_size = 100  # const
decisions = 5835  # decisions in 2023 (check on https://www.saos.org.pl/analysis)
pages = int(decisions / page_size) + 1
year = 2023  # to set
basic_url = "https://www.saos.org.pl/api/dump/judgments?pageSize=" + str(page_size) + "&judgmentStartDate=" + str(
    year) + "-01-01&judgmentEndDate=" + str(year + 1) + "-01-01"

loaded_data = get_data_pages(pages, basic_url)


len(loaded_data)


def load_n_decisions(n, page_size, year):
    pages = int(decisions / page_size) + 1
    params = {'pageSize': str(page_size), 'judgmentStartDate': str(year) + '-01-01'}
    basic_url = "https://www.saos.org.pl/api/dump/judgments?"
    loaded_data = get_data_pages(pages, basic_url, params)
    return loaded_data

loaded_data2 = load_n_decisions(5835, 100, 2023)

loaded_data[-1]["id"]
loaded_data2[-3]["id"]
loaded_data2[-2]["id"]
loaded_data2[-1]["id"]
# two additional ones?

# %% what if we take too many items

experiment = get_data(
    "https://www.saos.org.pl/api/dump/judgments?pageSize=100&judgmentStartDate=2020-01-01&judgmentEndDate=2020-01-02")[
    "items"]
len(experiment)  # 33 even i though we took 100 items and it still works

# %% counting decisions

# itemki - n pages from 01-01-2022
itemki = req(10)

decisions = 0
for i in range(len(itemki)):
    if itemki[i]["decision"] != None:
        decisions += 1
print(decisions)
print(len(itemki))

d1 = get_data("https://www.saos.org.pl/api/dump/judgments?pageSize=10&judgmentStartDate=2020-01-01")["items"]
d2 = \
get_data("https://www.saos.org.pl/api/dump/judgments?pageSize=10&judgmentStartDate=2020-01-01&withGenerated=false")[
    "items"]
type(d1)
e1 = d1[0]
e2 = d2[0]

e1.keys()
e2.keys()

d1[1]["referencedCourtCases"]

set(e1)

set(e1).difference(set(e2))


# %% everything to csv
import pandas as pd

selected_columns = ['id', 'courtType', 'courtCases', 'judgmentType', 'judges', 'source', 'courtReporters', 'decision', 'summary', 'textContent', 'legalBases', 'referencedRegulations', 'keywords', 'referencedCourtCases', 'receiptDate', 'meansOfAppeal', 'judgmentResult', 'lowerCourtJudgments', 'division', 'judgmentDate']
df = pd.DataFrame(columns=selected_columns)

loaded_data[0].keys()

orzeczenia_num = len(loaded_data)
for i in range (orzeczenia_num):
    df.loc[len(df)] = list(loaded_data[i].values())
    
df.to_csv("2023_orzeczenia.csv")


#%% does not work - TODO

import numpy as np
row = np.empty(len(selected_columns))
row.fill(np.NaN)

for i in range(len(loaded_data)):
    i=0
    df1.loc[i] = row
    for feature in selected_columns:
        #df1.loc[i, feature] = loaded_data[i][feature]



