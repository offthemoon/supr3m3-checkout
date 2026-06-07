''''
GmailSignIn NOTES. 

Notes on this.
We are going to want to allow the user to sign into a google/youtube account.

Will make solving the captcha easier. (Potential one clicks)
'''





#We are going to want to have the user sign in to their Gmail account to access their emails and perform actions on them.
#After the user signs in, want to verify that it stays signed in. 
from playwright.sync_api import sync_playwright
import os

#We are going to want to have the user sign in. 
def signIn():

    #Where we are going to want to store the user data. 
    user_data_dir = "./chromeInformation"  # Specify the path to your user data directory
    #Uses the OS module to check if the directory exists, and if it doesn't
    #We are going to create a new folder to store the user data. 
    if not os.path.exists(user_data_dir):
        os.makedirs(user_data_dir)
        print("Created a new Folder to store the your google information ..... ")
    

    
    with sync_playwright() as p:
        #We are going to want to launge the browswer with the data information. 
        #Cut this one out and launch actual chrome browser instead of the default one that comes with playwright.
        #browswer = p.chromium.launch_persistent_context(user_data_dir, headless=False)

        browswer = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            #will use the default installed google chrome path
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"  # Set custom user-agent  # Use the dynamically found Chrome path
        )

        browswer.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
    
    #Creates a new page in the browser context.
        page = browswer.new_page()

        #Set a custom user-agent to mimic a real browser
        #Navigate to Gmail login page.
        page.goto("https://accounts.google.com/signin")

        #Wait for the user to sign in and for the inbox page to load.
        page.wait_for_url("https://mail.google.com/mail/u/0/#inbox", timeout=60000)  # Wait for the inbox page to load, adjust timeout as needed

        #Verify that above passed and we are signed in. 
        print("We have sucessfully signed into the the gmail account. ")

        #We are going to save this information 
        #Needs to close the browswer to fully save the information. 
        browswer.close()

    return True