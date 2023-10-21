# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 10:47:53 2023

@author: biuro
"""

# pip install requests

import requests

# Define the URL of the REST API
api_url = "https://www.saos.org.pl/api/dump/judgments"

try:
    # Send an HTTP GET request to the API URL
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON data from the response
        data = response.json()

        # Now you can work with the JSON data as a Python dictionary
        # For example, print the first 10 items
        for item in data['items']:
            print(item)

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
    

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

