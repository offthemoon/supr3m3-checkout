#We are now going to have a function that is all about gettings a user profile and storing it.

#before this we are going to  want to load all the users profiles from a file into the arrary userProfiles.

import sqlite3


#The array of profiles that we have going to have store them all. 
userProifles = []

class UserProfile:
    profile_name = ""

    email = ""
    first_name = ""
    last_name = ""
    shipping_address = ""
    shippeing_address_2 = ""
    city = ""
    state = ""
    zip_code = ""
    country = ""    
    phone_number = ""

    #Now this is private information we are going to want the user to enter their payment info.
    card_number = ""
    card_expiry = ""
    card_cvv = ""
    name_on_card = ""


#We are going to create a database connection to store profiles.
main_db = sqlite3.connect('profiles.db')
cursor = main_db.cursor()


#This is going to creat the table if it does not exist. (That stores all the profiles info)
cursor.execute('''CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_name TEXT,
    email TEXT,
    first_name TEXT,
    last_name TEXT,
    shipping_address TEXT,
    shipping_address_2 TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    country TEXT,
    phone_number TEXT,
    card_number TEXT,
    card_expiry TEXT,
    card_cvv TEXT,
    name_on_card TEXT
)''')


#Now for this we are going to want to search through the database and load all the profiles into the userProfiles array.

def load_profiles():
    cursor.execute("SELECT * FROM profiles")
    rows = cursor.fetchall()
    for row in rows:
        #Creates a new object for each profile and adds it to the userProfiles array.
        profile = UserProfile()
        profile.profile_name = row[1]
        profile.email = row[2]
        profile.first_name = row[3]
        profile.last_name = row[4]
        profile.shipping_address = row[5]
        profile.shippeing_address_2 = row[6]
        profile.city = row[7]
        profile.state = row[8]
        profile.zip_code = row[9]
        profile.country = row[10]
        profile.phone_number = row[11]
        profile.card_number = row[12]
        profile.card_expiry = row[13]
        profile.card_cvv = row[14]
        profile.name_on_card = row[15]
        userProifles.append(profile)



def display_profiles():
    #Calls the function to load profiles from the database.
    load_profiles()
    print("Here is the profiles you currently have: ")

    print(userProifles)
    if userProifles.count == 0:
        print("No profiles found.")
    else:   
        for profile in userProifles:
            print(f"profile_name {profile.profile_name}, Email: {profile.email}, Name: {profile.first_name} {profile.last_name}, Address: {profile.shipping_address}, {profile.city}, {profile.state}, {profile.zip_code}, {profile.country}, Phone: {profile.phone_number}")





if __name__ == "__main__":

    print("Profile module loaded.")
    print("Please enter your email: ")
    user_email = input().strip()

