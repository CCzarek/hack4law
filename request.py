# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 10:47:53 2023

@author: biuro
"""

# pip install requests

import requests

# Define the URL of the REST API
api_url = "https://www.saos.org.pl/api/dump/judgments?pageSize=100&judgmentStartDate=2020-01-01"

try:
    # Send an HTTP GET request to the API URL
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON data from the response
        data = response.json()

        # Now you can work with the JSON data as a Python dictionary
        # For example, print the first 10 items
        #for item in data['items']:
        #    print(item)

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
    
    
#%% data dowload functions
    
def get_data(url):
    api_url = url
    try:
        response = requests.get(api_url)
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

def get_data_pages(pages, url):
    data = []
    for i in range(pages):
        url += "&pageNumber=" + str(i)
        data_add = get_data(url)["items"]
        if data_add != None:
            data += get_data(url)["items"]
    return data
# returns concatenated lists of items (dicts) available to pickle

#%% saving results
import pickle

# Function to save a list to a file using pickle
def save_list_to_file(file_name, my_list):
    try:
        with open(file_name, "wb") as file:
            pickle.dump(my_list, file)
        print(f"List saved to {file_name}")
    except Exception as e:
        print(f"Error saving list to file: {e}")

# Function to load a list from a file using pickle
def load_list_from_file(file_name):
    try:
        with open(file_name, "rb") as file:
            loaded_list = pickle.load(file)
        return loaded_list
    except Exception as e:
        print(f"Error loading list from file: {e}")
        return []

# Sample list
my_list = [1, 2, 3, 4, 5]

# Save the list to a file
save_list_to_file("my_list.pkl", my_list)

# Load the list from the file
loaded_list = load_list_from_file("my_list.pkl")

print("Original List:", my_list)
print("Loaded List:", loaded_list)

#%% loading all decisions from one year

page_size = 100 # const
decisions = 5835 # decisions in 2023 (check on https://www.saos.org.pl/analysis)
pages = int(decisions / page_size) + 1
year = 2023 # to set
basic_url = "https://www.saos.org.pl/api/dump/judgments?pageSize=" + str(page_size) + "&judgmentStartDate=" + str(year) + "-01-01&judgmentEndDate=" + str(year + 1) + "-01-01"
loaded_data = get_data_pages(pages, basic_url)
len(loaded_data)

save_list_to_file("data2023.pkl", loaded_data)
loaded_list = load_list_from_file("data2023.pkl")

loaded_data == loaded_list

#%% ?    

itemki = req(10)


print(data.keys)
data.keys()

['links', 'items', 'queryTemplate', 'info']

data["links"]
data["items"]
type(data["items"])
data["items"][0]
type(data["items"][0])
data["items"][0].keys()
# data["items] = data + extract features as dict keys
len(data["items"])

data["queryTemplate"]
data["info"]
type(data["info"])

#%% what if we take too many items

experiment = get_data("https://www.saos.org.pl/api/dump/judgments?pageSize=100&judgmentStartDate=2020-01-01&judgmentEndDate=2020-01-02")["items"]
len(experiment) # 33 even i though we took 100 items and it still works

#%% counting decisions

decisions = 0
for i in range(len(itemki)):
    if itemki[i]["decision"] != None:
        decisions += 1
print(decisions)
print(len(itemki))

d1 = get_data("https://www.saos.org.pl/api/dump/judgments?pageSize=10&judgmentStartDate=2020-01-01")["items"]
d2 = get_data("https://www.saos.org.pl/api/dump/judgments?pageSize=10&judgmentStartDate=2020-01-01&withGenerated=false")["items"]
type(d1)
e1 = d1[0]
e2 = d2[0]

e1.keys()
e2.keys()

d1[1]["referencedCourtCases"]

set(e1)

set(e1).difference(set(e2))

#%% test

save_list_to_file("my_list.pkl", d1)
loaded_list = load_list_from_file("my_list.pkl")

loaded_list
