#We are going to want to update profiles  for the task we are dealing with....

import os
import json
import main

#Will be a dictonary so we can display everything at once.
def displayOneProfile(profile):

    print("-------------------------------------------------------------------------------------------------")
    print("Profile Unique Number -> ", profile["Unique Number"])
    print("Profile name -> ", profile["Profile Name"])
    print("First Name -> ", profile["First Name"])
    print("Last Name -> ", profile["Last Name"])
    print("Address -> ", profile["Address"])
    print("Apartment -> ", profile["Apartment"])
    print("Zip Code -> ", profile["Zip Code"])

    #Credit Card information.....
    print("Credit Card -> ", profile["Credit Card"])
    print("Expiration Date -> ", profile["Expiration Date"])
    print("Security Code -> ", profile["Security Code"])


    print("-------------------------------------------------------------------------------------------------")



def loadAllProfilesThanMainMenu():
     #------------------------------------------------Locates the information in our JSON file --------------------------------------------------------------
    if os.path.exists("profiles_supreme.json"):
        with open("profiles_supreme.json", "r")  as file:
            prev_info = json.load(file)
    else:
        print("You have no profiles currently! ")
        return


    #Will go through the profiles one by one and display there information. 
    for profile in prev_info:
        print("-------------------------------------------------------------------------------------------------")
        print("Profile Unique Number -> ", profile["Unique Number"])
        print("Profile name -> ", profile["Profile Name"])
        print("First Name -> ", profile["First Name"])
        print("Last Name -> ", profile["Last Name"])
        print("Address -> ", profile["Address"])
        print("Apartment -> ", profile["Apartment"])
        print("Zip Code -> ", profile["Zip Code"])

        #Credit Card information.....
        print("Credit Card -> ", profile["Credit Card"])
        print("Expiration Date -> ", profile["Expiration Date"])
        print("Security Code -> ", profile["Security Code"])


        print("-------------------------------------------------------------------------------------------------")
        
        #No longer need this... we are improving our flow. 
       #main.main_menu()



#this is going to display all the profiles
def loadProfiles():

    #------------------------------------------------Locates the information in our JSON file --------------------------------------------------------------
    if os.path.exists("profiles_supreme.json"):
        with open("profiles_supreme.json", "r")  as file:
            prev_info = json.load(file)
    else:
        print("You have no profiles currently! ")
        return


    #Will go through the profiles one by one and display there information. 
    for profile in prev_info:
        print("-------------------------------------------------------------------------------------------------")
        # print("Profile Unique Number -> ", profile["Unique Number"])
        #Make this green so the user can see it easier. 
        print("\033[92mProfile Unique Number ->\033[0m", profile["Unique Number"])
        print("Profile name -> ", profile["Profile Name"])
        print("First Name -> ", profile["First Name"])
        print("Last Name -> ", profile["Last Name"])
        print("Address -> ", profile["Address"])
        print("Apartment -> ", profile["Apartment"])
        print("Zip Code -> ", profile["Zip Code"])

        #Credit Card information.....
        print("Credit Card -> ", profile["Credit Card"])
        print("Expiration Date -> ", profile["Expiration Date"])
        print("Security Code -> ", profile["Security Code"])


        print("-------------------------------------------------------------------------------------------------")

   
#Going to create a new profile. 
def createProfile():

    #For this we are going to want to create a new profile.....
    #For this need to load the old files and store the
    print("You want to add a new profile .... ")
    userInput = input("Please [Q] to cancel or press anything else to continue with adding a profile : ").lower()

    if userInput == "q":
        return
    

    profile = {}
    new_profile_updated = [] 

    file_path = "profiles_supreme.json"

    #------------------------------------------------Locates the information in our JSON file --------------------------------------------------------------
    if os.path.exists(file_path):
        with open(file_path, "r")  as file:
            new_profile_updated = json.load(file)

    #This is going to get how many we have already .... will add it to the key for uniqueniss.
    count = len(new_profile_updated)

    #All the users inputs. 
    user_profile_name = input("Please enter your profile name (Try to make it unique if you can ): ").lower()
    user_email_address = input("Email Address: ").lower()
    user_first_name = input("Please enter your first name: ").lower()
    user_last_name = input("Please enter your last name: ").lower()
    user_address_name = input("Please enter your Shipping address name: ").lower()
    user_apartment_number = input("Please enter your apartment # of leave blank: ").lower()
    user_city = input("Your City: ").lower()
    user_state = input("Your state: ").lower()
    user_zipcode_name = input("Please enter your ZipCode: ").lower()
    user_phone_number = input("Phone Number: (813-xxx-xxxx) format")

    user_Credit_card = input("Credit Card #: ")
    user_Experiation_Date = input("Experiation Date: month / year (mm / yy) e.g. 12/25")
    user_CSV = input("Enter security Code: ")



    #Now we want this dictonary to be mapped 

    profile = {"Unique Number": count+1 , 
            "Email": user_email_address,
            "Profile Name" : user_profile_name, 
            "First Name": user_first_name, 
            "Last Name": user_last_name, 
            "Address": user_address_name, 
            "Apartment": user_apartment_number,
            "City" : user_city,
            "State" : user_state,
            "Zip Code": user_zipcode_name,
            "Phone Number": user_phone_number,
            "Credit Card":user_Credit_card,
            "Expiration Date": user_Experiation_Date,
            "Security Code": user_CSV
            }
    
    #We are going to want to append our profile to the list that contains all our dictonaries.
    new_profile_updated.append(profile)

    #After this we are going to want to write to our json file


    with open(file_path, "w") as file:
           json.dump(new_profile_updated,file,indent =2)
           print("Profile Successfully added! ")


def LocateProfile(unique_key):

        print("\033[92mWe are locating the profile associated with -> \033[0m", unique_key)

        if os.path.exists("profiles_supreme.json"):
            with open("profiles_supreme.json", "r")  as file:
                prev_info = json.load(file)
        else:
            print("You have no profiles currently! ")
            return
        
        for profile in prev_info:
            if profile["Unique Number"] == int(unique_key):
                return profile

        print("\033[91mWe couldn't locate the profile associated with that Key! \033[0m")
        return 0
        


    
