from __future__ import print_function

# Import libraries
import time 
import requests
import cv2
import operator
import numpy as np
import pandas as pd
import xmltodict


# Variables for the Computer Vision
_region = 'francecentral' #Here you enter the region of your subscription
_url = 'https://{}.api.cognitive.microsoft.com/vision/v2.0/analyze'.format(_region)
_key = None #Here you have to paste your primary key
_maxNumRetries = 10

global urlImage #Here we will store the image URL
global json #This will be part of the request to the Computer Vision 

# Set the Computer Vision parameters
params = { 'visualFeatures' : 'Description'} 

headers = dict()
headers['Ocp-Apim-Subscription-Key'] = _key
headers['Content-Type'] = 'application/json' 


# Open the Media XML file that was generated with WordPress Export
with open('test.wordpress.image.feed.xml') as fd: #Using _test.xml file for testing
    
    raw = xmltodict.parse(fd.read())

# Create a dictionary from the items in the XML
data_x = [[r["title"], r["guid"]["#text"], r["description"]] for r in raw["rss"]["channel"]["item"]]
print("Number of images", len(data_x)) 

# Does the actual results request to the Computer Vision API
def processRequest( json, data, headers, params ):

    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )

        if response.status_code == 429: 

            print( "Message: %s" % ( response.json() ) )

            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                result = None 
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                if 'application/json' in response.headers['content-type'].lower(): 
                    result = response.json() if response.content else None 
                elif 'image' in response.headers['content-type'].lower(): 
                    result = response.content
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json() ) )

        break
        
    return result


# Loop in the dictionary and send the request to the Computer Vision 
for k in data_x:
    print(k[1])  #Print URL of the image

    urlImage = k[1] 
    json = { 'url': urlImage } #Here is the json for sending out the request

    data = None

    result = processRequest( json, data, headers, params )
    print(result)
 
# Extract the caption if available

    if result is not None:
        if 'description' in result:
            description = result['description']['captions'][0]['text']
            k[2] = description #Replace Description value 
            print(k[2])  #Print Description   

df = pd.DataFrame(data_x, columns=["title", "url", "description"])
df.to_csv("out.csv", encoding='utf-8', index=False)
print("Results saved on CSV")

