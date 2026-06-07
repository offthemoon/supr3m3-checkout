#We are going to make a shopfiy bot. 
import MonitorOLD
import Profile_User
import profileManager
import Task
import user_captcha
import SignIn
import time

#We are going to want this as the main file that runs everything.
#Whenever we have import files this is going to load all the files code outsise of functions.
#global variables used for the login. 
attempts = 0 
result = False


#We are going to want to now use something called loggers (To keep track on data information....)
def main_menu():
        
        # ---> We are going to want to have while true. The reason why is because 
        #We are going to want the user be able to select again. 
        user_choice = 'default'

        while(user_choice != 'q'):

            print("----- Main Menu of BlackBox AIO version 1.1 ------")

            print("Please press [1] to look at your profiles. ")

            print("Please enter [2] to add a profile ")

            #Going to want to give the user some options here to choose from.
            print("Please press [3] to create a task to monitor a website for Supreme. ")

            print("Please press [4] for the sams club module ")

            print("Please press [5] for your two captcha key ")

            print("Please press [6] to update your two captcah key ")

            print("Please press [7] to sign into your gmail account (important against reCaptcha)! ")

            print("Please press [8] to update your discord URL for notifications. ")

            print("Please press [9] to test your webhook URL for notifications. ")

            print("Please press [10] to add Topps Accounts... ")

            print("Please press [11] to run the topps module...")

            print("Please press [P] for proxy tab / information ")

            print("Please enter [Q] to exit the program. ")

            user_choice = input("Enter your choice: ").strip().lower()

            if user_choice == '1':
                #Load all profiles (if any) and display them
                profileManager.loadAllProfilesThanMainMenu()
                print("End of profiles list.    ")

            elif user_choice == "2":
                profileManager.createProfile()
                
            elif user_choice == '3':
                Task.StartTask()

            elif user_choice == '4':
                import samsClub
                print("Sams Club Is currently In beta Testing -> Canno't use right now.")
                #samsClub.SamsClubSignIn()
                
            elif user_choice == '5':
                user_captcha.readCaptcahKey()
            elif user_choice == '6':
                user_captcha.changeCaptchaKey()

            elif user_choice == '7':
                import GmailSignIn
                GmailSignIn.signIn()

            elif user_choice == '8':
                import discordWebHook
                discordWebHook.updateDiscordURL()

            elif user_choice == '9':
                import discordWebHook
                discordWebHook.testWebHook()
            
            elif user_choice == '10':
                import ToppsModule
                ToppsModule.AddAccount()

            elif user_choice == '11':
                print("Currently UnderConstruction.... avaliable (2.0) version")
                # import ToppsModule
                # ToppsModule.settingModule()

            elif user_choice == 'p':
                import proxy
                proxy.proxyMainMenu()
                
            
            elif user_choice == 'q':
                print("Shutting down application....")

        
            #Task module will handle monitoring websites.



if __name__ == "__main__":

    print("Welcome to Elite AIO! Created By OfftheMoon! ")

    print(r"""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║   ███████╗██╗     ██╗████████╗███████╗                       ║
    ║   ██╔════╝██║     ██║╚══██╔══╝██╔════╝                       ║
    ║   █████╗  ██║     ██║   ██║   █████╗                         ║
    ║   ██╔══╝  ██║     ██║   ██║   ██╔══╝                         ║
    ║   ███████╗███████╗██║   ██║   ███████╗                       ║
    ║   ╚══════╝╚══════╝╚═╝   ╚═╝   ╚══════╝                       ║
    ║                                                              ║
    ║   █████╗ ██╗ ██████╗                                         ║
    ║  ██╔══██╗██║██╔═══██╗                                        ║
    ║  ███████║██║██║   ██║                                        ║
    ║  ██╔══██║██║██║   ██║                                        ║
    ║  ██║  ██║██║╚██████╔╝                                        ║
    ║  ╚═╝  ╚═╝╚═╝ ╚═════╝                                         ║
    ║                                                              ║
    ║                 Version 1.1                                  ║
    ║        Created and Maintained by OffTheMoon                  ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    #Testing ... uncomment this.

    #result = True

    #Would we attempt anything for this? 
    #How do we get the user in order to return back to main menu. 
    while attempts < 3 and result == False:

        #Get the result by calling helper function of SignIn to have the user enter the key and return True or False -> depending on it worked or not. 
        result = SignIn.signIn()

        #Increment attempt by 1 -> only allowing a user 3 times to try before shutting down.  
        if not result:
            attempts += 1

    if result == True:
        main_menu()
    else:
        print("Invalid username or password. Please try again later or contact a developer. ")
        








