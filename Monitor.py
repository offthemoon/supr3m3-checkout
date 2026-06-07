#This is going to be to monitor the website.... notice for any 
import requests
import test
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


from playwright.sync_api import sync_playwright

import os



# ...existing code...

def find_item_by_keywords(driver, keywords):
    """Search the page for elements matching the given keywords.

    Args:
        driver: Selenium WebDriver instance.
        keywords: List of keywords to search for in product titles.
    
    Returns:
        str: Full product URL if found, None if not found.
    """

    print("[DEBUG] Searching for keywords:", keywords)

    BASE_URL = "https://www.supremenewyork.com"

    try:
        # Wait for products to load on the page first
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt]"))
        )

        # Build XPath — ALL keywords must be in the alt text (case-insensitive)
        # translate() converts alt text to lowercase so matching is case-insensitive


        #Converts all the websites info to lower case. This is important because the user may input keywords in any case, and we want to ensure that the search is case-insensitive.
        def make_contains(term: str) -> str:
            return (
                f"contains("
                f"translate(@alt, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
                f"'{term.lower()}')"
            )

        #Joins all the conditions.
        conditions = " and ".join(make_contains(k) for k in keywords)
        xpath = f"//img[{conditions}]"


        # Find ALL matching images
        matching_images = driver.find_elements(By.XPATH, xpath)

        # No matches found
        if len(matching_images) == 0:
            print(f"[INFO] No products matched keywords: {keywords}")
            return None


        # Grab the first matching image
        product_image = matching_images[0]
        matched_alt = product_image.get_attribute("alt")

        # Walk up DOM to the parent <a> tag to get the href
        product_link_element = product_image.find_element(
            By.XPATH, "./ancestor::a[@data-testid='react-router-link']"
        )

        href = product_link_element.get_attribute("href")

        # href could be relative "/products/abc" or full "https://..."
        if href.startswith("http"):
            product_url = href
        else:
            product_url = BASE_URL + href

        print(f"[SUCCESS] Found product URL: {product_url}")
        return product_url

    except Exception as e:
        print(f"[ERROR] find_item_by_keywords failed: {e}")
        return None


# Optional: notifications (Discord webhook)
# Set your webhook URL in the environment variable `DISCORD_WEBHOOK_URL`


DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL', '').strip()

# If you prefer to hard-code the webhook (not recommended), you can set
# `DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/…'` here.

def send_discord_notification(message: str):
    """Send a message to the configured Discord webhook.

    Tries modern `SyncWebhook` (discord.py v2+), then legacy `Webhook` with
    `RequestsWebhookAdapter`, then falls back to a direct HTTP POST.

    If `DISCORD_WEBHOOK_URL` is not set the function is a no-op.
    """
    if not DISCORD_WEBHOOK_URL:
        print("[DEBUG] DISCORD_WEBHOOK_URL not set; skipping webhook send.")
        return

    # Try discord.py v2+ SyncWebhook
    try:
        from discord import SyncWebhook
        print(f"[DEBUG] Sending Discord webhook via SyncWebhook to {DISCORD_WEBHOOK_URL[:60]}...")
        webhook = SyncWebhook.from_url(DISCORD_WEBHOOK_URL)
        webhook.send(message)
        print("[DEBUG] Discord webhook sent successfully (SyncWebhook).")
        return
    except Exception as e:
        print(f"[DEBUG] SyncWebhook failed or unavailable: {e}")

    # Try legacy Webhook with RequestsWebhookAdapter
    try:
        from discord import Webhook, RequestsWebhookAdapter
        print(f"[DEBUG] Sending Discord webhook via Webhook/RequestsWebhookAdapter to {DISCORD_WEBHOOK_URL[:60]}...")
        webhook = Webhook.from_url(DISCORD_WEBHOOK_URL, adapter=RequestsWebhookAdapter())
        webhook.send(message)
        print("[DEBUG] Discord webhook sent successfully (Webhook).")
        return
    except Exception as e:
        print(f"[DEBUG] Webhook/RequestsWebhookAdapter failed or unavailable: {e}")

    # Fallback to HTTP POST
    try:
        resp = requests.post(DISCORD_WEBHOOK_URL, json={"content": message}, timeout=10)
        if resp.status_code in (200, 204) or resp.ok:
            print("[DEBUG] Discord POST fallback succeeded.")
        else:
            print(f"[ERROR] Discord POST fallback failed: {resp.status_code} {resp.text}")
    except Exception as e2:
        print(f"[ERROR] Discord POST fallback exception: {e2}")


def monitor_website(users_input,user_profile, size,base_url, check_interval=60):
    """
    Monitors the specified website for availability.
    
    Parameters:
    url (str): The URL of the website to monitor.
    check_interval (int): The interval in seconds between checks.
    """
    # Set up Chrome options for headless browsing

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

    #First want to determine if the users input (URL is going to be a keyword or URl)
    is_url = users_input.startswith("http://") or users_input.startswith("https://")

    print(f"[DEBUG] is URL: {is_url}, user input: {users_input}")

    #If the input was not detected to be a URL....
    if not is_url:
        print("[INFO] Input does not appear to be a URL. Will attempt keyword search instead and return the URL.")

        #Parse the keywords. 
        users_input = users_input.split("+")  # Assuming keywords are separated by +

        #Now we are going to want to create a new list 
        keywords = []

        for k in users_input:
            #Remove all the spaces and make it smaller. 
            keywords.append(k.strip().lower())

        if not keywords:
            print("[ERROR] No valid keywords provided. Please check your input and try again.")
            return
            
        #Create a temporary driver to search for the item URL based on keywords.
        driver = webdriver.Chrome(options=chrome_options)
        try:
            driver.get(base_url)
            users_input = find_item_by_keywords(driver, keywords)
        except Exception as e:
            print(f"[ERROR] Failed during keyword search: {e}")
            users_input = None
        finally:
            driver.quit()


    #Will catch that we coudln't find a url. 
    if users_input is None:
        print("[ERROR] Could not find a URL matching the keywords. Please check your input and try again.")
        return
  
    #Going to add something else that will allow the user to break out of it. 
    while True:
        #For this new implementation we are going to not want to use the URL
        #We are going to want to use keywords to find the the item of itself. 
        #First we can use a if url do this....
            try:
                driver = webdriver.Chrome(options=chrome_options)
                driver.get(users_input)
                
                # Wait for the add to cart button or sold out message to appear
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "button"))
                    )
                except:
                    pass
                
                page_content = driver.page_source.lower()
                
                # More reliable stock detection
                in_stock_indicators = [
                    'add to cart',
                    'add to bag',
                    'in stock',
                    'button[aria-label*="add"]'
                ]
                
                out_of_stock_indicators = [
                    'out of stock',
                    'sold out',
                    'unavailable',
                    'coming soon'
                ]
                
                is_in_stock = any(indicator in page_content for indicator in in_stock_indicators)
                is_out_of_stock = any(indicator in page_content for indicator in out_of_stock_indicators)
                
                if is_in_stock and not is_out_of_stock:
                    alert_message = f"[ALERT] {users_input} is IN STOCK!"
                    print(alert_message)

                    print("Trying to checkout!!! ")

                    #new developement treatment just in case if there is an error we can go back to monitoring item.
                    #CheckOut(users_input,user_profile,size)

                    #--------------new modification to checkout logic --------------------

                    try: 
                        CheckOut(users_input,user_profile,size)

                    except  Exception as e:
                        print("Coudl't checkout! Trying again. ")

                    #------------new modification to checkout logic ----------------------

                    #End of new information
                    # Debug: confirm we're about to call the webhook sender
                    print("[DEBUG] about to call send_discord_notification()")
                    # Send Discord webhook notification if webhook function is available
                    try:
                        send_discord_notification(alert_message)
                    except Exception as e:
                        print(f"[ERROR] send_discord_notification() raised: {e}")
                elif is_out_of_stock:
                    print(f"[INFO] {users_input} is out of stock.")
                else:
                    print(f"[INFO] {users_input} is up and running (stock status unknown).")
                
                driver.quit()
                
            except Exception as e:
                print(f"[ERROR] Could not reach {users_input}. Exception: {e}")
                try:
                    driver.quit()
                except:
                    pass
            
            sleep(check_interval)
       


if __name__ == "__main__":
    # interactive entrypoint — safe to import Monitor without running this block
    print("Please enter the wbsite URL to monitor: ") 
    website_url = input().strip()
    print("Please enter the check interval in seconds (default is 60): ")
    interval_input = input().strip()
    check_interval = int(interval_input) if interval_input.isdigit() else 60
    #monitor_website(website_url, check_interval)
    print("Monitoring started...")

# Now if its stock lets have a self bot that can add to cart and checkout


def CheckOut(URL,userProfile,size):

    print("Trying to cart item to cart... ")


    with sync_playwright() as p:
        #Creates a new browswer with google chrome. 

        #We are going to launch the browser with the data information. (Signed In google account)
        #browser = p.chromium.launch(headless=False,slow_mo=100,channel="chrome")

        #Reload Information/ data from the user data directory so we can have the most up to date information.
        user_data_dir = "./chromeInformation" 

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

        #this browswer we opened is now going to create a new page. 

        page = browswer.new_page()

        #goes to this new page....
        page.goto(URL)

        #We are going to want to find the label with the name size... and select the option that matches our size 
        page.get_by_label("size").select_option(label=size)

        page.get_by_role("button", name="add to cart").click()

        Checkout_action = page.get_by_test_id("mini-cart-checkout-link")
        
        Checkout_action.wait_for(state="visible")

        Checkout_action.click()


        #To help with the queue system. -> Implemented and we are going to see if this is actually a correct way to do it.


        try:
            # Wait for the queue page to appear
            queue_element = page.wait_for_selector("text=Queue", timeout=2500)  # Adjust timeout as needed
            if queue_element:
                print("Queue detected. Waiting for it to complete...")
                # Wait for the queue to complete (e.g., wait for a specific element to appear)
                page.wait_for_selector("text=Continue to Checkout", timeout=900000)  # Adjust timeout as needed
                print("Queue completed. Proceeding to checkout...")
        except Exception:
            print("No queue detected. Proceeding to checkout...")


        #Now we are going to fill in everything from this...
        email = userProfile["Email"]

        First_name =  userProfile["First Name"]
        Last_name =  userProfile["Last Name"]
        Address = userProfile["Address"]
        Apartment =  userProfile["Apartment"]
        City =  userProfile["City"]
        State = userProfile["State"]
        ZipCode = userProfile["Zip Code"]
        PhoneNumber =  userProfile["Phone Number"]

        Credit_Card = userProfile["Credit Card"]
        Expiration_Date = userProfile["Expiration Date"]
        Security_Code = userProfile["Security Code"]



        #Now for this we are going to possible get a captcha proccess that we are going to have
        #To do hCaptcha to solve for this...

        page.get_by_placeholder("email").type(email,delay=170)
        page.get_by_placeholder("first name").type(First_name,delay=150)
        page.get_by_placeholder("last name").type(Last_name,delay=130)
        page.get_by_placeholder("address").type(Address,delay=170)
        page.get_by_placeholder("apt").type(Apartment,delay=155)
        page.get_by_placeholder("city").type(City,delay=178)

        #Checkout_action.get_by_placeholder("first name").type(State,delay=350)

        page.get_by_placeholder("postal code").type(ZipCode,delay=150)
        page.get_by_placeholder("phone").type(PhoneNumber,delay=150)


        #most credit cards are protected by an Iframe so must use this isntead

        #First locate the iframe field by it's box / name. 
        card_number_frame = page.frame_locator("iframe[title='Field container for: Card number']")
        card_number_frame.get_by_placeholder("Card number").type(Credit_Card, delay=150)

        #card_number_frame.get_by_placeholder("expiration date").type(Expiration_Date,delay=150)


        #Expiration date 
        Expiration_date = page.frame_locator("iframe[id^='card-fields-expiry-']")
        Expiration_date.get_by_placeholder("expiration date ").type(Expiration_Date,delay=150)

        #Security Code Time

        # <iframe class="card-fields-iframe" frameborder="0" id="card-fields-verification_value-cemq5avxtz000000" 
        # name="card-fields-verification_value-cemq5avxtz000000" scrolling="no"
        # src="https://checkout.pci.shopifyinc.com/build/739af4d/verification_value-ltr.html?identifier=&amp;locationURL=" 
        # title="Field container for: Security code" style="height: 44px;"></iframe>

        security = page.frame_locator("iframe[id^='card-fields-verification_value-']")
        security.get_by_placeholder("security code").type(Security_Code,delay=150)

        #Name On card time 

        #<iframe class="card-fields-iframe" frameborder="0" id="card-fields-name-5dfdl9vz2vu00000" name="card-fields-name-5dfdl9vz2vu00000" scrolling="no" 
        #src="https://checkout.pci.shopifyinc.com/build/739af4d/name-ltr.html?identifier=&amp;locationURL=" title="Field container for: Name on card" style="height: 44px;"></iframe>

        FullName = First_name + " " + Last_name

        name = page.frame_locator("iframe[id^='card-fields-name-']")
        name.get_by_placeholder("name on card").type(FullName,delay=220)



        #Here we are going to want the to press the submit button....

        # <button aria-busy="false" aria-live="polite" id="checkout-pay-button" 
        # type="submit" class="_1m2hr9ge _1m2hr9gd _1fragemz7 _1fragemsm _1fragemur _1fragemyk _1fragemz0 _1fragemz2 _1fragemyr _1fragemuw _1m2hr9g1p _1m2hr9g1l _1fragemul _1m2hr9g1f _1m2hr9g1c _1fragemyq _1m2hr9g1z _1m2hr9g1x _1m2hr9g15 _1m2hr9g13 _1m2hr9gh _1m2hr9gf _1fragem32 _1m2hr9g1w _1m2hr9g19 _1m2hr9g17 _1fragemvp _1m2hr9g1k"><span class="_1m2hr9gv _1m2hr9gu _1fragemyf _1fragemyw _1fragemyq _1fragemz3 _1m2hr9gr _1m2hr9gp _1fragem3c _1fragem87 _1fragemyi">
        # process payment</span></button>

        #Wait 2500 seconds to make sure the page is fully loaded and we are past any queue system.
        #Waits for the button to appear before we click it.
        page.get_by_role("button", name="process payment").wait_for(state="visible")


        page.get_by_role("button", name="process payment").click()

        #page.frame_locator("iframe[title='Field container for: Name on card']")

        #We are going to want to send a discord notification and let the user know we checked out. 



        #Now we are going to want to send a webhook if the new user has checkedout (We are going to assume they did)

        test.sendWebHook(URL,size,userProfile)

        print('We made it past here....')







        



    

    



