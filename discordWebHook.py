import main
import os
import requests
import json



def add_new_webhook():

    with open("discordURL.json", "w") as f:
        print("Please enter your discord URL for notifications. ")
        discord_url = input("Enter your discord URL: ").strip()

        #this is the format JSON stores. 
        info = {"Discord_URL": discord_url}
        #We are going to add to this now the URL to the file.
        json.dump(info, f, indent=1)
        print("Saved your discord URL successfully. ")
        #Instead of waiting around we are going to want to ensure it's written in quickly. 
        f.flush()
        main.main_menu()

def updateDiscordURL():

    #If this does not exist we are going to create a new file to store the discord URL.
    if not os.path.exists("discordURL.json"):
        with open("discordURL.json", "w") as f:
            print("You have no stored discord URL, Please enter your discord URL for notifications. ")
            discord_url = input("Enter your discord URL: ").strip()

            #this is the format JSON stores. 
            info = {"Discord_URL": discord_url}

            #We are going to add to this now the URL to the file.
            json.dump(info, f, indent=1)
            f.flush()
            print("Saved your discord URL successfully. ")

            main.main_menu()


    else:
        with open("discordURL.json", "r") as f:
            #Get all the information from the file and store it in a variable.
            #Extract the discord URL. 
            try:
                information = json.load(f)
                current_url = information["Discord_URL"]
                print(f"Your current stored discord URL is: {current_url}")
                print("Do you want to update it? (y/n)")
                choice = input("Enter your choice: ").strip().lower()
                if choice == 'y':
                    new_url = input("Enter your new discord URL: ").strip()
                    with open("discordURL.json", "w") as f:
                        f.write(new_url)
                        print("Discord URL updated successfully.")

                        #ReDirect back to main 
                        main.main_menu()

                else:
                    print("Discord URL not updated.")
                    main.main_menu()

            #If the file is not in the correct format, we are going to catch the error and ask the user to update their URL or delete the file and try again.
            except json.JSONDecodeError:
                print("The file is not in the correct format, please update your discord URL. Or delete the file and try again. ")
                add_new_webhook()
                
                print("Redirecting you back to the main menu. ")
                main.main_menu()
 

def testWebHook():

    try: 
        with open("discordURL.json", "r") as f:
            information = json.load(f)
            discord_url = information["Discord_URL"]
            print(f"Testing your discord URL: {discord_url}")

            #This is the JSON payload that we are going to use to send to the discord.
            # Content -> What the image will sned
            # Username -> The name that will appear on the discord message
            #  Avatar_url -> The image that will appear on the discord message (must be a direct image URL, not a webpage URL)
         

            #Actually send the POST request to the discord URL with the JSON payload.
            #requests.post(discord_url, json=webookInfo)
            #Here we would add code to send a test message to the discord URL to verify it works.
    except FileNotFoundError:
        print("The file does not exist .... please enter your discord URL first. ")
        main.main_menu()

    except json.JSONDecodeError:
        print("The file is not in the correct format, please update your discord URL. Or delete the file and try again. ")
        add_new_webhook()

        print("Redirecting you back to the main menu. ")
        main.main_menu()
        
    
