# NewEgg.com WebScraper And Crawler For Laptops
## April 2020


![intro_pic0](./images/logo.jpg)

![intro_pic2](./images/bs4_logo.png)

![intro_pic1](./images/selenium-python-splinter.jpg)


## Scope & Purpose

* For this project, I built a Newegg.com laptop web scraper and page crawler program that succesfully scraped 25 and 47 pages, with 900 and 1,692 laptops scraped including their: brand, product category, image (link), model specifications and details, product links, item numbers, current promotion information (if applicable), price, and page number. In the processing folder, you will each page from Newegg that was scraped, concatenated CSV files from both scraping sessions in the output folder. There are built in functions to alert the user when Newegg suspects a bot via sound effects, and provides suggested actions to circumvent their defenses. This is a supervised web crawler and scraper that is 80% automated, and requires 20% or less effort from the user. Once the scraper is setup, it is possible to leave the scaper in the running in the background should you desire to multitask. The objective for this project was to further develop my data mining and Python skills, and build a robust webscraper with the limited time I invested into this project. Data extraction from the web (the "E" in ETL) is an essential skill as a Data Engineer and analyst, and that was my main focus for this project.


## Background Information

* My inspiration came from an YouTube video called "Introduction To WebScraping With Python and BeautifulSoup", uploaded by Data Science Dojo Channel, and it instructed by Mr. Phuc Duong, Sr. Data Science Engineer. When I was finding my way on how to build a web scraper, this video that began the snowball effect of my progress. I will post the link in the credits at the end. Although this video was made 3 years ago, and versions of Python and BeautifulSoup he used were older, Mr. Duong did a great job in explaining the underlying concepts of webscraping with BeautifulSoup. I was able to reproduce the same results, go more in-depth, and even add my own flare to it by referring to updated documenation. After achieving initial success of scraping one page of laptops from Newegg, I wanted to further challenge myself by building a web crawler capability that automatically loops through as many pages as my search query produced, scrape all the targeted laptop data, and output a CSV file for each page and a list Python objects. To reach this goal, I decided to use Splinter for the following reasons: Splinter is wrapper on top of Selenium that is Python based (Selenium does have a Python library, however it is originally JavaScript based according to https://python.libhunt.com/compare-splinter-vs-selenium); Splinter is said to be gaining popularity; and Python is my natural strength. I found that Splinter and the Chrome Web Driver relatively easy to implement to automate my program. Thoughout my program, I also made a genuine effort to weave in dyanmic and object oriented programming concepts, which I found made my code more scalable, efficient, and stylistically cleaner.


## System Prerequisites To Get Started

You will need the following installed on your computer system and import the following libraries:
* Python >= 3.7
* import os
* import re
* import glob
* import time
* import random
* import requests
* import datetime
* import pandas as pd
* from re import search
* from splinter import Browser
* from playsound import playsound
* from bs4 import BeautifulSoup as soup
* Jupyter Notebook - all of the programming reside in these files


## Getting Started - Two Options

* Only Viewing The Source Code And Produced Results - please click on the Jupyter Notebook in the repository to view all of my code, webcrawler and scraper program. I've also saved the results log from my program when I completed a 47 page scrape in the txt file. In the final_ouputs and processing folder, you will see the 25 and 47 page successful scrapes my program produced saved as CSV files.

* Clone / Download Entire Repository - if you'd like to replicate my work or even use the scraper yourself, please download / clone my repository and install all of the prerequisites. After, you can open the Jupyter Notebook, use the same search query I did or go to Newegg.com, and input a search URL you queried yourself from the site. The Jupyter Notebook allows you to run everything cell by cell, incase you need to make any tweaks. I'd recommend scraping towards midnight for the best results, which is explained more in the "Encountering Potential Errors" section below.


## Main Built-in Functionalities

* NewEgg Web Scarper Functions - this function will keep trying to scrape the target page using a combination of while loop, random sleep patterns to emulate human behavior, and try and excepts. The output are a CSV file per scraped page; all laptops on a page are then passed into a Laptop class, and instances of these objects  are created using a list comprehension, and are subsequently appended to a list called "product_catalog", producing a "list of list of objects".

* Splinter Webcrawler Functions - accurately loops thru pages of the search result; decides to randomly mouse over product links on pages by "flipping a coin" every page that is iterated through; and randomly sleeps and clicks the top or bottom next page button to emulate human behavior.

* Concatenation Function - enables the user concatenate all scarped pages in the processing folder into one CSV file after entire scrape is completed, and is saved in the final_outputs folder. Note: as of right now, anything in the processing folder will be concatenated unless physically moved out or cleared, which segways to the function below.

* Clear Processing Folder Function - enables the user to clear out the "processing" folder to prevent clutter; I opted not to clear the this folder and intentionally left / moved files in files back into the processing folder as an example.

* Google reCAPTCHA and NewEgg's "Are You Human?" Test Functions - these scans the requested HTML, pauses the program, and alerts the user if Newegg suspects a bot and provides suggested actions to help the user circumvent Newegg's defenses to be successful in their scrape. I created these because I kept running into exceptions and errors, and I wanted to find ways around them by first catching, implementing what I refer to as a "break pedal", to give user an opportunity to manually circumvent the errors, if my try and excepts do not work. This is why I called this a "supervised scrape".


## Expectations - User Inputs And Outputs

* Input requirement from the user is Step 3 in the picture below, which the user goes to Newegg.com, selects preferred laptop specifications and clicks apply, and copy and pastes the search query results's URL into the program when prompted.

![user_input1](./images/input2.PNG)

* Outputs:

1) Each Scraped page as a seperate CSV file in the processing folder

![user_input1](./images/processing_folder.PNG)

2) One CSV file of all pages scraped in one CSV file in the final_output folder

![user_input1](./images/finshed_outputs.PNG)


## Program Preview And Findings

* Welcome to NewEgg.com Supervised Web Crawler and Scraper - please see an example of the introduction to the program and where and how the user will be asked to input the URL to their custom laptop search query.

![program_start](./images/0_scraperwelcome.PNG)

* After the user input a search query URL, here is a sample of what to expect as when the program is web scraping, and crawling down the page and over to the next.

![scraping_inprogress](./images/scraping_inprogress.PNG)

* Laptops in the yellow square is what the scraper targets every page.

![scraping_inprogress](./images/dual_screen_zoomout.PNG)

* Examples Of Top And Bottom Next Page Buttons The Web Crawler Randomly Targets Page-To-Page By "Flipping A Coin".

![button_top](./images/topbutton.PNG)

* Note: For the Bottom Next Page Button - I found that NewEgg.com had more of a tendency to change bottom divs when you get deep into the scrape especially, when it suspects the user is a bot, or after the user was prompted to take a Google reCAPTCHA test.

![button_bottom](./images/bottombutton.PNG)
**
* Programmed "Break Pedals" - the program will pause and user will be alerted when Newegg suspects the user is a bot. After the user takes necessary actions to by pass it, the user is asked to enter in any key to attempt to continue the scrape. Below are examples:

![button_bottom](./images/breakpedal_topbottom_nextpg_notworking.PNG)
**

## Encountering Potential Errors

* Newegg's uses Google's reCAPTCHA to help protect websites from being webscraped by requiring site visitors to prove they're human by completing image identification tests. As you can imagine, this was the most difficult obstacle about this project I had to figure out a way to overcome, which is why this why I call this a "supervised webscraper and crawler", as the user is prompted to take action to circumvent their defenses. I also found that the timing of when you decide to scrape is also important. I strongly hypothesize Newegg employs machine learning along with Google's reCAPTCHA to predict which users are bots scraping their data based on all users traffic and actions from that day. As you may know, most commerical websites collect data on how long users are on their page, which links they interact with, and etc. With this said, I found that when I scraped late around midnight, was when I had the best results and was most successful.
  
- Google reCAPTCHA Test Example Below:

![recaptcha_test](./images/recaptcha_test.PNG)


* Post reCAPTCHA Test - Passed And the Scraper Continues Example Below:

![recaptcha_test_passed](./images/recaptcha_alert_passed.PNG)

* Additional notes regarding scraping errors - Every time I made an attempt to scrape Newegg.com, it got harder and harder. I believe this is because in addition to using Google reCAPTCHA, they also have JavaScript triggers to load elements at certain times or based on certain user actions. I do beleive they use machine learning as well and compare your actions based on an entire days worth of data. I found the JavaScript does sometimes change up certain div tags for the next page buttons. Another pattern I noticed is after completing a "Are you human?" test, Newegg would send a bogus HTML on the back end to BeautifulSoup4, which causes an Index Error for the scraper. To circumvent this, the program automatically refresh the page, and establishing a manual break using an input function, where you the user would take the suggested action (e.g. add an item to a cart as if you were shopping, and navigate using the back button to the page where you left off). The "Are you human?" function will trigger next, and scan the new requested text for bogus unscrapabe "Are you human?" HTML, as seen in the picture below. The "Are you human?" function would then be recursively called again, to scan the new requested HTML after briefly sleeping, and if it passes, the program will continue. 

* "Are you human?" HTML - Example Of Bogus HTML On The Backend:

![bogus_HTML](./images/areyouhuman_request.PNG)


## Next Steps Considerations

* Reiterate on loops, put top and bottom xpaths into a list, and create a loop including tries and excepts instead of manually brute forcing. Goal would be to cut down redundant code and make it more elegant.
  
* Create nice charts and data visualizations with the data.

* Learn how to use Selenium which is the OG to Splinter - perhaps for my next project.


### Personal Note

* Hope you enjoyed it. Thank you for your time!

## Author

* **Johneson Giang** - *Invidual Project* - [Github](https://github.com/jhustles)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments & Credits

* Shout out to Mr. Phuc Duong for the great video that helped inspire this project - Sr. Data Science Engineer @ Data Science Dojo - https://www.youtube.com/watch?v=XQgXKtPSzUI

* I definitely want to give a shout out to my dear teacher, mentor, and friend @CodingWithCorgis!