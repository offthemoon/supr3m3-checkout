#We are going to want to validate the users information 
import requests

import time

#Should this information be protected? Can it be published?
#This URL is going to be where u place ur cloudflare worker url (I used it for this. )
URL = ""

def signIn():
    
    #Going to extract the users input as a key... strip it to remove any spaces before or after hand. 
    user_key = input("Enter your key (Press [Q] to Quit): ").strip()

    #If user enters q or Q -> going to shut down and quit the application. 
    if user_key == "Q" or user_key == 'q':
        print('Quitting Application.... ')
        exit()
    

    #Request and see what the code is. 
    r = requests.post(URL, json={"key": user_key}, timeout=10)


    #Verify the request was smooth. 
    if r.status_code != 200:
        print("There was an error validating your key, please try again later. ")
        return False
    
    #Extract data if request went. 
    data = r.json()

    #Data is going to be in the format of {"ok": true} or {"ok": false} depending on if the key is valid or not.
    #Returns {"ok": true} if the key is valid, and {"ok": false} if the key is invalid.
    if not data.get("ok"):

        #added some infomration..
        print('working..... ****')
        #added this information. 

        print("Your key is not valid, please enter a valid key.")
        return False
    
    print("Your key is valid, you have successfully signed in.")
    return True
