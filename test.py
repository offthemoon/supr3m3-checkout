    #We are going to want to test our application 

import requests

#Test URL we are going to want to use to see if it works. 
URL = 'https://us.supreme.com/products/4ij4d82mq9z-_3w2'

#Where you are also going to place ur WORKER URL (For the webhooks to be sent via cloudflare)
worker_url = ''

from bs4 import BeautifulSoup

#So given this URL we are going to want to test if our application can extract the image from the page and use it for the 
#Avatat url for discord 

#If we do not recieve a profile_name we are going to want to default and set it to Null.
def sendWebHook(URL,size = 'N/A',profile_name = 'Null'):

    #First we are going to want to get the information from the URL. 
    #We are going to want to get the image and we are going to want to get the item name. 

    #We are going to use beatiful soup to extract all the informaiton                               ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    info = requests.get(URL)
    #Going to want to do some more information for this currently right now. (Like Error handling)
    #Convert it to the text information. 
    html = info.text

    #Now we are going to want to use soup to grab the html. 
    soup = BeautifulSoup(html,'html.parser')

    #Now we can find the information associated with the ITEM in the URL.
    item_name = soup.find('h1').text

    #Now we are going to want to find the stuff associated with the image.
    item_image_url = soup.find('img')
    item_image_url = item_image_url['src']
    #Now this is a real URL link where we can grab the information....
    item_image_url = 'https:' + item_image_url

    #This is going to be the default amount of information we are going to be associated.

    print(profile_name, 'This is the profile name we are dealing with right now')


    #The contents of the webohook is going to be based on this below. 
    web_hook_information = {}

    #I wonder if there is actuallly a better way to catch this type of information / errror. 
    if profile_name == 'Null':
        web_hook_information = {
            'item_title' : item_name,
            'item_url' : item_image_url,
            'profile_name' : "Null",
            'email' : "Null",
            'size' : size
        }
       
    else:
        web_hook_information = {
            'item_title' : item_name,
            'item_url' : item_image_url,
            'profile_name' : profile_name['Profile Name'],
            'email' : profile_name['Email'],
            'size' : size
        }

    #Send the requst to our helper -> so they can post the webhook to our main information. 
    response = requests.post(worker_url,json=web_hook_information)

    print(response.status_code)
