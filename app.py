#!/usr/bin/env python
# coding: utf-8

# # NewEgg.Com WebCrawler & Scraper Program For Laptops - Beta v1.0
# 
# ###  - April 29th, 2020
# 
# #### By: Johneson Giang
# 
# ---

# In[1]:


# Import dependencies

import os
import re
import glob
import time
import random
import requests
import datetime
import pandas as pd

from re import search
from splinter import Browser
from playsound import playsound
from bs4 import BeautifulSoup as soup


# In[2]:


# Reminder to self.
#import this


# ## Functions & Classes Setup
# ---

# In[3]:


# Return date throughout the program.

def return_dt():
    
    global current_date
    
    current_date = str(datetime.datetime.now()).replace(':','.').replace(' ','_')[:-7]
    
    return current_date

#return_dt()


# In[4]:


"""
Main NewEgg WebScraper function - outputs are csv file and Laptop objects.

"""

def newegg_page_scraper(containers, turn_page):
    
    page_nums = []
    
    general_category = []
    
    product_categories = []
    
    images = []
    
    product_brands = []
    
    product_models = []
    
    product_links = []
    
    item_numbers = []
    
    promotions = []
    
    prices = []
    
    shipping_terms = []
    
    # Set gen_category as a global variable to make it accessible throughout the program, and to avoid an error.
    
    global gen_category
    
    """ 
    Loop through all the containers on the HTML, and scrap the following content into the following lists
    
    """
    for con in containers:
        
        try:
            
            page_counter = turn_page
            
            page_nums.append(int(turn_page))
            
            gen_category = target_page_soup.find_all('div', class_="nav-x-body-top-bar fix")[0].text.split('\n')[5]
            
            general_category.append(gen_category)
            
            prod_category = target_page_soup.find_all('h1', class_="page-title-text")[0].text
            
            product_categories.append(prod_category)
            
            image = con.a.img["src"]
            
            images.append(image)

            prd_title = con.find_all('a', class_="item-title")[0].text
            
            product_models.append(prd_title)

            product_link = con.find_all('a', class_="item-title")[0]['href']
            
            product_links.append(product_link)
            
            shipping = con.find_all('li', class_='price-ship')[0].text.strip().split()[0]
            
            if shipping != "Free":
                
                shipping = shipping.replace('$', '')
                
                shipping_terms.append(shipping)
                
            else:
                shipping = 0.00
                
                shipping_terms.append(shipping)

            brand_name = con.find_all('a', class_="item-brand")[0].img["title"]
            
            product_brands.append(brand_name)

        except (IndexError, ValueError) as e:
            
            # If there are no item_brand container, take the Brand from product details.
            
            product_brands.append(con.find_all('a', class_="item-title")[0].text.split()[0])

        try:
            current_promo = con.find_all("p", class_="item-promo")[0].text
            
            promotions.append(current_promo)
            
        except:
            
            promotions.append('null')

        try:
            price = con.find_all('li', class_="price-current")[0].text.split()[0].replace('$','').replace(',', '')
            
            prices.append(price)
            
        except:
            price = 'null / out of stock'
            
            prices.append(price)

        try:
            item_num = con.find_all('a', class_="item-title")[0]['href'].split('p/')[1].split('?')[0]
            
            item_numbers.append(item_num)
            
        except (IndexError) as e:
            item_num = con.find_all('a', class_="item-title")[0]['href'].split('p/')[1]
            
            item_numbers.append(item_num)    
    
    # Convert all of the lists into a dataframe
    
    df = pd.DataFrame({
    'item_number': item_numbers,
    'general_category': general_category,
    'product_category': product_categories,
    'brand': product_brands,
    'model_specifications': product_models,
    'price': prices,
    'current_promotions': promotions,
    'shipping': shipping_terms,
    'page_number': page_nums,
    'product_links': product_links,
    'image_link': images
    })
    
    # Rearrange the dataframe columns into the following order.
    df = df[['item_number', 'general_category','product_category', 'page_number' ,'brand','model_specifications' ,'current_promotions' ,'price' ,'shipping' ,'product_links','image_link']]
    
    # Convert the dataframe into a dictionary.
    
    global scraped_dict
    
    scraped_dict = df.to_dict('records')
    
    # Grab the subcategory "Laptop/Notebooks" and eliminate any special characters that may cause errors.
    
    global pdt_category
    
    pdt_category = df['product_category'].unique()[0]
    
    # Eliminate special characters in a string if it exists.
    
    pdt_category = ''.join(e for e in pdt_category if e.isalnum())
    
    """ Count the number of items scraped by getting the length of a all the models for sale.
        This parameter is always available for each item-container in the HTML
    """

    global items_scraped
    
    items_scraped = len(df['model_specifications'])

    """
    Save the results into a csv file using Pandas
    """
    
    df.to_csv(f'./processing/{current_date}_{pdt_category}_{items_scraped}_scraped_page{turn_page}.csv')
    
    # Return these variables as they will be used.
    
    return scraped_dict, items_scraped, pdt_category


# In[5]:


def web_Scraper_part2():
    
    x = random.randint(6, 10)
    
    def rdm_slp_6_10(x):

        time.sleep(x)

        print(f"Mimic Humans - Sleeping for {x} seconds. ")

        return x    
    
    
    keep_trying = True
    
    try_counter = 0
    
    while keep_trying == True:
    
        try:
            
            try_counter += 1
            
            target_url = browser.url
            
            rdm_slp_6_10(x)

            response_target = requests.get(target_url)

            print(f"{response} \n")

            target_page_soup = soup(response.text, 'html.parser')

            are_you_human_backend(target_page_soup)
            
            newegg_page_scraper(containers, turn_page)

        except IndexError as e:

            # Usually puts out JavaScriptionExceptions not errors

            print(f"EXCEPTION - Neweggscraper function error:| {e} | \n")

            playsound('./sounds/break_pedal.wav')
            
            rdm_slp_6_10(x)
            
            break_pedal_2 = input("Exception - WEBSCRAPER - Break pedal - manually refresh the page, and perhaps add an item to the cart, and go back to the same page where you left off and resume the scrape. \n")
            

        else: # Execute this if no exception is raised. Set keep trying to false.
            
            keep_trying = False
            
            print(f"After {try_counter} attempts, SUCCESSFULLY scraped the page and will continue... \n")
            
            print(f"Scraped Current Page: {turn_page} \n")
            
            #global scraped_dict
            
            return scraped_dict, items_scraped, pdt_category


# In[6]:


# Function to return the total results pages.

def results_pages(target_page_soup):
    
    # Use BeautifulSoup to extract the total results page number.
    
    results_pages = target_page_soup.find_all('span', class_="list-tool-pagination-text")[0].text.strip()
    
    #print(results_pages)
    
    # Find and extract total pages + and add 1 to ensure proper length of total pages.
    
    global total_results_pages
    
    total_results_pages = int(re.split("/", results_pages)[1])
    
    return total_results_pages


# In[7]:


"""
Build a function to concatenate all pages that were scraped and saved in the processing folder.
Save the final output (1 csv file) all the results
    
"""
def concatenate(total_results_pages):
    
    path = f'./processing\\'
    
    scraped_pages = glob.glob(path + "/*.csv")
    
    concatenate_pages = []
    
    counter = 0
    
    for page in scraped_pages:
        
        df = pd.read_csv(page, index_col=0, header=0)
        
        concatenate_pages.append(df)

    compiled_data = pd.concat(concatenate_pages, axis=0, ignore_index=True)
    
    total_items_scraped = len(compiled_data['brand'])
    
    concatenated_output = compiled_data.to_csv(f"./finished_outputs/{current_date}_{total_items_scraped}_scraped_{total_results_pages}_pages_.csv")
    
    return


# In[8]:


"""
Built a function to clear out the entire processing files folder to avoid clutter.
Or the user can keep the processing files (page by page) for their own analysis.

"""
def clean_processing_fldr():
    
    path = f'./processing\\'
    
    scraped_pages = glob.glob(path + "/*.csv")
    
    if len(scraped_pages) < 1:
        
        print("There are no files in the folder to clear. \n")
        
    else:
        
        print(f"Clearing out a total of {len(scraped_pages)} scraped pages in the processing folder... \n")
        
        clear_processing_files = []
        
        for page in scraped_pages:
            
            os.remove(page)
        
    print('Clearing of "Processing" folder complete. \n')
    
    return


# In[9]:


# Mouse over function to go thru hover over product links on the page to emulate humans.

def random_a_tag_mouse_over3():
    
    x = random.randint(6, 10)
    
    def rdm_slp_6_10(x):

        time.sleep(x)

        print(f"Mimic Humans - Sleeping for {x} seconds. ")

        return x    

    working_try_atags = []
    
    finally_atags = []

    working_atags = []

    not_working_atags = []

    try_counter = 0

    finally_counter = 0
    
    time.sleep(1)
    
    # Mouse over to header of the page "Laptops"
    
    browser.find_by_tag("h1").mouse_over()
    
    number_of_a_tags = len(browser.find_by_tag("a"))
    
    # My observation has taught me that most of the actual laptop clickable links on the grid are in the <a> range 2000 to 2100.
    if number_of_a_tags > 1900:
        
        print(f"Found {number_of_a_tags} <a> tags when parsing html... ")
        
        random_90_percent_plug = (random.randint(90, 94)/100.00)
        
        start_a_tag = int(round((number_of_a_tags * random_90_percent_plug)))
        
        end_a_tag = int(round((number_of_a_tags * .96)))
        
    else:
        
        # After proving you're human, clickable <a>'s sometimes are reduced 300, so adjusting mouse_over for that scenario.

        print(f"Found {number_of_a_tags} <a> tags when parsing html... ")
        
        random_40_percent_plug = (random.randint(40, 44)/100.00)
        
        start_a_tag = int(round((number_of_a_tags * random_40_percent_plug)))
        
        end_a_tag = int(round((number_of_a_tags * .46)))

    step = random.randint(13, 23)
    
    for i in range(start_a_tag, end_a_tag, step):

        try: # try this as normal part of the program - SHORT

            rdm_slp_6_10(x)

            browser.find_by_tag("a")[i+2].mouse_over()

            time.sleep(3)

        except: # Execute this when there is an exception

            print("EXCEPTION raised during mouse over. Going to break loop and proceed with moving to the next page. \n")

            break

        else: # execute this only if no exceptions are raised

            working_try_atags.append(i+2)

            working_atags.append(i+2)

            try_counter += 1

            print(f"<a> number = {i+2} | Current Attempts (Try Count): {try_counter} \n")


    return


# In[10]:


# Checks for Google's reCaptcha "are you human?" test and alerts the user.

def g_recaptcha_check():
    
    if browser.is_element_present_by_id('g-recaptcha') == True:
        
        for sound in range(0, 2):
            
            playsound('./sounds/user_alert.wav')
        
        print("recaptcha - Check Alert! \n")
        
        continue_scrape = input("Newegg system suspects you are a bot. \n Complete the recaptcha test to prove you're not a bot. After, enter in any key and press ENTER to continue the scrape. \n")
        
        print("Continuing with scrape... \n")
        
    return


# In[11]:


# Created an are you human backend test bc Newegg would send bogus "are you human" html when "requesting" for html.

def are_you_human_backend(target_page_soup):
    
    if target_page_soup.find_all("title")[0].text == 'Are you a human?':
        
        playsound('./sounds/user_alert.wav')

        print("Newegg suspects you're a bot on the backend. Automatically will refresh, and target new URL. \n")
        
        print("Refreshing page. Please wait... \n")
        
        for i in range(0, 1):
            
            browser.reload()
            
            time.sleep(2)
        
        browser.back()
        
        print("Sleeping for 30 seconds to emulate humans. \n")
        
        time.sleep(30)
        
        browser.forward()
        
        playsound('./sounds/break_pedal.wav')
        
        break_pedal_ayh = input("Please click a laptop item, and add or remove it from the cart, and go back to the same page using the back button of your browser. \n Then enter in any key and press enter to continue scraping. \n")
        
        # Allocate time for page to load. 
        
        time.sleep(3)
            
        print("Targeting new url... ")
            
        # After user passes test, target the new url, and return updated target_page_soup.
        
        target_url = browser.url

        response_target = requests.get(target_url)

        target_page_soup = soup(response_target.text, 'html.parser')
        
        # Recursively call the function, and if it passes, continue on with the program.
        
        are_you_human_backend(target_page_soup)
        
    else:
        
        print("Passed the 'Are you human?' check when requesting and parsing the html. Continuing with scrape ... \n")
        
        # Otherwise, return the target_page_soup that was passed in.
        
        return target_page_soup


# In[12]:


# crazy idea, put links in a list, and then loop thru them and try and except else (break out of the loop) and continue

def random_xpath_top_bottom():
    
    x = random.randint(3, 8)
    
    def rdm_slp_3_8(x):

        time.sleep(x)

        print(f"Slept for {x} seconds. \n")

        return x
    
    coin_toss_top_bottom = random.randint(0,1)
    
    next_page_button_results = []
    
    # If the coin toss is even, mouse_over and click the top page link.
    
    if (coin_toss_top_bottom == 0):
        
        try:
        
            print('Heads - Clicking "Next Page" Top Button. \n')

            x = random.randint(3, 8)

            print(f"Mimic human behavior by randomly sleeping for {x}. \n")

            rdm_slp_3_8(x)

            browser.find_by_xpath('/html/body/div[4]/section/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[2]/button').mouse_over()

            time.sleep(1)

            browser.find_by_xpath('/html/body/div[4]/section/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[2]/button').click()

            next_page_button_results.append(coin_toss_top_bottom)

            print('Heads - SUCCESSFUL "Next Page" Top Button. \n')

            return
        
        except:
            
            print("EXCEPTION - Top Next Page button mouse over and click UNSUCCESSFUL... ")
        
            try:

                x = random.randint(3, 8)

                print(f"Mimic human behavior by randomly sleeping for {x}. \n")

                rdm_slp_5_9(x)

                print('Attempting to click the bottom "Next Page" Xpath Bottom Button. \n')
                
                browser.find_by_xpath('/html/body/div[4]/section/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[4]/div/div/div[11]/button').mouse_over()

                time.sleep(4)

                browser.find_by_xpath('/html/body/div[4]/section/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[4]/div/div/div[11]/button').click()

                print('EXCEPTION BYPASSED - Bottom Next Page Button SUCCESSFUL! \n')

            except:

                print("EXCEPTION - Top and Bottom Next Page Button Link not working... \n")

                playsound('./sounds/break_pedal.wav')

                break_pedal_xptb = input("Break Pedal - Please manually click next page. Then enter in any key and press enter to continue the scrape. \n ")

                print("Continuing... \n")

                print("="*60)
        
        return
            
    else: # If coin toss is tails or 1, then...
        
        try:
            
            print('Tails - Clicking "Next Page" Xpath Bottom Button. \n')

            x = random.randint(3, 8)

            print(f"Mimic human behavior by randomly sleeping for {x}. \n")

            rdm_slp_5_9(x)

            browser.find_by_xpath('/html/body/div[4]/section/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[4]/div/div/div[11]/button').mouse_over()
                              
            time.sleep(4)

            browser.find_by_xpath('/html/body/div[4]/section/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[4]/div/div/div[11]/button').click()

            print('Tails - 1st Bottom Xpath - SUCCESSFUL "Next Page" Bottom Button. \n')
            
        except:
            
            print("EXCEPTION - 1st Bottom Xpath Failed. Sleep for 4 second then will try with 2nd Xpath bottom link. \n")
        
        try:
            
            time.sleep(4)
            
            browser.find_by_xpath('/html/body/div[4]/section/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[3]/div/div/div[11]/button').mouse_over()
            
            time.sleep(4)
            
            browser.find_by_xpath('/html/body/div[4]/section/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[3]/div/div/div[11]/button').click()
            
            print('EXCEPTION BYPASSED! Tails - 2nd Bottom Xpath - SUCCESSFUL "Next Page" Bottom Button. \n')
            
        except:
            
            print("EXCEPTION - 2nd Bottom Xpath Failed. Trying with 3rd Xpath bottom link. \n")
        
        try:
            time.sleep(4)
            
            browser.find_by_xpath('/html/body/div[5]/section/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[4]/div/div/div[11]/button').mouse_over()
            
            time.sleep(4)
            
            browser.find_by_xpath('/html/body/div[5]/section/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[4]/div/div/div[11]/button').click()
                      
            print('EXCEPTION BYPASSED!  Tails - 3rd Bottom Xpath - SUCCESSFUL "Next Page" Bottom Button. \n')
        
        except:
            
            print("Last Bottom Next Page Xpath Button was unsuccessful... Will Attempt Top Next Page Button.... \n")
            
        try:

            x = random.randint(3, 8)

            print(f"Mimic human behavior by randomly sleeping for {x}. \n")

            rdm_slp_3_8(x)

            browser.find_by_xpath('/html/body/div[4]/section/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[2]/button').mouse_over()

            time.sleep(1)

            browser.find_by_xpath('/html/body/div[4]/section/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[2]/button').click()

            next_page_button_results.append(coin_toss_top_bottom)

            print('EXCEPTION BYPASSED SUCCESSFUL "Next Page" Top Button worked. \n')

            return
        
        except:
            
            print("EXCEPTION BYPASSES UNSUCCESSFUL - All 3 Xpath Bottom Button AND Top Next Page Xpath Button was not working due to JavaScipt Exceptions... \n")
            
            playsound('./sounds/break_pedal.wav')
            
            break_pedal_xptb = input("Break Pedal - Please manually click the next page button. Then enter in any key and press enter to continue the scrape. \n ")

        return

    


# In[13]:


"""
This class takes in the dictionary from the webscraper function, and will be used in a list comprehension

to produce class "objects"

"""
class Laptops:
    
    counter = 0
    
    def __init__(self, **entries):
        
        self.__dict__.update(entries)
        
    def count(self):
        
        print(f"Total Laptops scraped: {Laptops.counter}")

"""
Originally modeled out parent/child inheritance object structure.

After careful research, I found it much easier to export the Pandas Dataframe of the results to a dictionary,

and then into a class object.

"""
# class Product_catalog:
    
#     all_prod_count = 0
    
#     def __init__(self, general_category): # computer systems
#         self.general_category = general_category
        
#         Product_catalog.all_prod_count += 1
        
#     def count_prod(self):
#         return int(self.all_prod_count)
#         #return '{}'.format(self.general_category)

# Sub_category was later changed to Laptops due to the scope of this project.
# class Sub_category(Product_catalog): # laptops/notebooks, gaming
    
#     sub_category_ct = 0
    
#     def __init__(self, general_category, sub_categ, item_num, brand, price, img_link, prod_link, model_specifications, current_promotions):
#         super().__init__(general_category)
#         Sub_category.sub_category_ct += 1
        
#         self.sub_categ = sub_categ
#         self.item_num = item_num
#         self.brand = brand
#         self.price = price
#         self.img_link = img_link
#         self.prod_link = prod_link
#         self.model_specifications = model_specifications
#         self.current_promotions = current_promotions


# ## Main Program Logic
# ---

# In[14]:


""" Welcome to the program message!
"""
print("=== NewEgg.Com Laptop - Supervised Web Crawler & Scraper Beta v1.0 ===")

print("=="*30)

print('Scope: This project is a beta and is only built to scrape the laptop section of NewEgg.com due to limited time. \n')

print("Instructions: \n")

return_dt()

print(f'Current Date And Time: {current_date} \n')

print("(1) Go to www.newegg.com, go to the laptop section, select your requirements (e.g. brand, screensize, and specifications - SSD size, processor brand and etc...) ")

print("(2) Copy and paste the url from your exact search when prompted ")

print('(3) This is a "Supervised Scraper", meaning it will mostly be automated, but you will be alerted to take action when necessary. ')

print('(4) You may run the program in the background after the initial set of instructions, as the program will alert you to take action (e.g. when Newegg suspects a bot. )')

print('(5) After the webscraping is successful, you will have an option to concatenate all of the pages you scraped together into one csv file')

print('(6) Lastly, you will have an option to clear out the processing folder (data scraped by each page)')

print('(7) If you have any issues or errors, "PRESS CTRL + C" to quit the program in the terminal ')

print('Disclaimer: Newegg may ban you for a 24 - 48 hours for webscraping their data, then you may resume. \n Also, please consider executing during the day, with tons of web traffic to their site in your respective area. \n')

print('Happy Scraping!')

# Set up Splinter requirements.

executable_path = {'executable_path': './chromedriver.exe'}

# Ask user to input in the laptop query link they would like to scrape.

url = input("Please copy and paste your laptop query that you want to webscrape, and press enter: \n")

browser = Browser('chrome', **executable_path, headless=False, incognito=True)

browser.visit(url)

# Allocating loading time.

time.sleep(3)

break_pedal_1 = input("Break Pedal - close any pop ups and go any item and add one to the cart and go to the first search query. ")

current_url = browser.url

response = requests.get(current_url)

print(f"{response} \n")

target_page_soup = soup(response.text, 'html.parser')

# Run the results_pages function to gather the total pages to be scraped.
results_pages(target_page_soup)

"""
This is the loop that performs the page by page scraping of data / results
of the user's query.
"""
# List set up for where class Laptop objects will be stored.

print("Beginning webscraping and activity log below... ")

print("="*60)

product_catalog = []

for turn_page in range(1, total_results_pages+1):
    
    """
    If "reCAPTCHA" pops up, pause the program using an input. This allows the user to continue
    to scrape after they're done completing the quiz by inputting any value.
    """
    # Allocating loading time.
    
    time.sleep(3)
    
    # Check if the site believes we are a bot, if so alert the user to take action.
    
    g_recaptcha_check()

    print(f"Beginning mouse over activity... \n")
    
    # Set up "containers" to be passed into main scraping function. 
    
    if turn_page == 1:
        
        containers = target_page_soup.find_all("div", class_="item-container")
        
        # Added this and moved it here to test new setup.
        newegg_page_scraper(containers, turn_page)
        
    else:
        
        web_Scraper_part2()
        
    print("Creating laptop objects for this page... \n")
    
    # Create instances of class objects of the laptops/notebooks using a list comprehension.
    
    objects = [Laptops(**prod_obj) for prod_obj in scraped_dict]
    
    print(f"Finished creating Laptop objects for page {turn_page} ... \n")
    
    # Append all of the objects to the main product_catalog list (List of List of Objects).
    
    print(f"Adding {len(objects)} to laptop catalog... \n")
    
    product_catalog.append(objects)
    
    print("Flipping coin to decide mouse over on the page or not... ")
    
    n = random.randint(0,1)
        
    if n == 0:
        
        print("Heads - will mouse over the page. ")
        
        random_a_tag_mouse_over3()
        
    else:
        
        r = random.randint(8, 20)
        
        print(f"Tails - will sleep for {r} seconds. and continue")
        
        time.sleep(r)

    #print("Will scrape pages, but will need to randomly sleep for max 35 seconds to emulate human behavior. \n")
    
    if turn_page == total_results_pages:
        
        print(f"Completed scraping {turn_page} / {total_results_pages} pages. \n ")
        
        # Exit the broswer once complete webscraping.
        
        browser.quit()
        
    else:
        
        try:
            
            y = random.randint(4, 6)
            
            print(f"Current Page: {turn_page}) | SLEEPING FOR {y} SECONDS THEN will click next page. \n")
            
            time.sleep(y)
            
            random_xpath_top_bottom()

        except:
            
            z = random.randint(3, 5)
            
            print(f" (EXCEPTION) Current Page: {turn_page}) | SLEEPING FOR {z} SECONDS - Will click next page, if applicable. \n")
            
            time.sleep(z)
            
            random_xpath_top_bottom()
            
    print("")
    print("="*60)
    print("")

# Prompt the user if they would like to concatenate all of the pages into one csv file

concat_y_n = input(f'All {total_results_pages} pages have been saved in the "processing" folder (1 page = csv files). Would you like for us concatenate all the files into one? Enter "y", if so. Otherwise, enter anykey to exit the program. \n')

if concat_y_n == 'y':
    
    concatenate(total_results_pages)
    
    print(f'WebScraping Complete! All {total_results_pages} have been scraped and saved as {current_date}_{pdt_category}_scraped_{total_results_pages}_pages_.csv in the "finished_outputs" folder \n')

# Prompt the user to if they would like to clear out processing folder function here - as delete everything to prevent clutter

clear_processing_y_n = input(f'The "processing" folder has {total_results_pages} csv files of each page that was scraped. Would you like to clear the files? Enter "y", if so. Otherwise, enter anykey to exit the program. \n')

if clear_processing_y_n == 'y':
    
    clean_processing_fldr()

print('Thank you checking out my project, and hope you found this useful! \n')

