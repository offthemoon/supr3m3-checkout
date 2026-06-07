
import os
import json

#from twocaptcha import TwoCaptcha

import main
from dotenv import load_dotenv
#we are going to want to store our captcha key with encrptin

from cryptography.fernet import Fernet

file_Name = "captchaInformation.json"
env_file_name = "secert.env"




#We are going to want to load our previous captcah informaition


#going to want to open our file system to see if we are going to have that captcha information
#This will always start whenever the program is called in main.... 
if os.path.exists(file_Name):
    with open(file_Name,"r") as File:
        captchaInformation = json.load(File)
    



def changeCaptchaKey():
    if os.path.exists(file_Name):
        with open(file_Name,"r") as File:
            captchaInformation = json.load(File)

            Captcha_key = captchaInformation["Two_Captcha_Key"]

            print("Captcha Key -> ", Captcha_key)

            print("Please enter the new key: ")
            new_key = input().strip()

            user_dict = {"Two_Captcha_Key" : new_key}

            with open(file_Name, "w") as File:

                json.dump(user_dict,File,indent=2)

                print("Succesfully updated your 2Captcha key! ")

                main.main_menu()

    else:
        print("You have no captcha key.... ")
        print("Please enter your captcha key: ")

        #We are going to take the users input.
        user_captcha_key = input().strip()
        

        #Opens/creates a path for writing too.
        with open(file_Name,"w") as File:
            #since json stores dictonarys we are going to put user_captcha key in it.
            user_dict = {"Two_Captcha_Key": user_captcha_key }

            json.dump(user_dict,File,indent=2)

            print("Succesfully updated your 2 Captcha Key!!! ")

def readCaptcahKey():

    if os.path.exists(file_Name):
        with open(file_Name, "r") as File:
            info = json.load(File)
            two_captcha_key = info["Two_Captcha_Key"] 
            print("2 Captcha key is -> ", two_captcha_key)
            main.main_menu()

    else:
        print("File could not be located .... please enter a key to create a file.")
        main.main_menu()













