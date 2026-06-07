#We are now going to want to start the task file that will handle the tasks for monitoring the website.

from time import sleep
import profileManager
import main 

import Monitor

#If the user from main clicked start task we are going to want to start our monitoring task.
def StartTask():

    print("You want to start a task. ")
    print("Press [Q] to return or press any button to contine ")
    userInput = input().lower()

    if userInput == "q":
        print("Returning to main menu... ")
        main.main_menu()
        return


    print("\033[92mPlease enter the Unique Key for the profile you want to use .... \033[0m")
    profileManager.loadProfiles()

    #We are going to get a digit that the unique profile is going to find to run... 
    userInput = input()
    user_profile = profileManager.LocateProfile(userInput)

    if user_profile == 0:
        print("Please try again")
        return
    
    print("Succesfully Found the associated profile with the unique key-> ", userInput)
    profileManager.displayOneProfile(user_profile)

    print("If this is the correct profile press any button, if wrong press [Q] ")

    userInput = input()

    if userInput == "q":
        return


   
    print("Please enter the check interval in seconds (default is 60): ")
    interval_input = input().strip()
    check_interval = int(interval_input) if interval_input.isdigit() else 60

    print("Please enter the size you want ")
    print("Small Enter [S] ")
    print("Medium Enter [M] ")
    print("Large Enter [L] ")
    print("Extra Large Enter [X] ")
    print("Random Size Press [R] ")

    print("If this is a shoe size just type the size you want....")

    #is going to get the size we are going to want to be watching for.....
    userInput = input().lower().strip()
    sizeKeyWord = ""

    if userInput == "s":
        sizeKeyWord = "Small"

    elif userInput == "m":
        sizeKeyWord = "Medium"

    elif userInput == "l":
        sizeKeyWord = "Large"

    elif userInput == "x":
        sizeKeyWord = "XLarge"
    
    elif userInput == "r":
        sizeKeyWord = "random"

    #if this is going to be a shoe want to determine what size. 
    elif userInput.isdigit():
        sizeKeyWord = userInput

    else:
        print("The word -> ", userInput, " doesn't match available sizes....")
        return
    

    print(""" Please Type The Corresponding Category It Will Be In   
    [1] Jackets
    [2] Shirts
    [3] tops/sweaters
    [4] sweatshirts
    [5] pants
    [6] t-shirts
    [7] hats
    [8] bags
    [9] accessories
    [10] shoes
    [11] Skate
          """)
    

    category_input = input().strip()
    

    #we know for python we can have a dictonary or a map. 
    
    answers = {

        "1": "https://us.supreme.com/collections/jackets",
        "2": "https://us.supreme.com/collections/shirts",
        "3": "https://us.supreme.com/collections/tops-sweaters",
        "4": "https://us.supreme.com/collections/sweatshirts",
        "5": "https://us.supreme.com/collections/pants",
        "6": "https://us.supreme.com/collections/t-shirts",
        "7": "https://us.supreme.com/collections/hats",
        "8": "https://us.supreme.com/collections/bags",
        "9": "https://us.supreme.com/collections/accessories",
        "10": "https://us.supreme.com/collections/shoes",
        "11": "https://us.supreme.com/collections/skate"

    }


    #Now that we have the created dictonary with the information extract the url

    if(category_input not in answers):
        print("The category you entered is not valid. Please try again.")
        main.main_menu()

    #Extract the url from the dictonary and store it in a variable to be used for monitoring.
    base_url = answers[category_input]

    
    
    print("Please enter the website URL to monitor or keywords!: ")
    website_url = input().strip()


    if not website_url:
        print("You must enter a valid URL or keywords to monitor.")
        return

     # ── Summary Before Starting ──────────────────────────────────────
    print(f"""
    ╔══════════════════════════════════════╗
    ║           TASK SUMMARY               ║
    ╠══════════════════════════════════════╣
    ║  Target  : {website_url[:38]}
    ║  Size    : {sizeKeyWord}
    ║  Interval: {check_interval}s
    ╚══════════════════════════════════════╝
    """)

    if input("Press ENTER to start or [Q] to cancel... ").lower() == "q":
        print("Task cancelled.")
        return
    
    #We are going want to have a waiting period here before we start the task so the user can read everything over and make sure it's correct.
    #Will pass this information onto
    print("[INFO] Starting task...")

    #def monitor_website(users_input,user_profile, size, base_url, check_interval=60):
    Monitor.monitor_website(website_url,user_profile,sizeKeyWord, base_url, check_interval)




