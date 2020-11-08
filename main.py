#NOTE: We can use WebDriverWait and EC.presence_of_element
#For simplicity sake, i have used sleep
# You can change the time of sleep as per speed of your net.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import datetime as dt
from datetime import timedelta
import time
import pandas as pd
opt = Options()
opt.add_argument("--disable-infobars")
# opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
# Pass the argument 1 to allow and 2 to block for permission pop ups.
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 2,
    "profile.default_content_setting_values.media_stream_camera": 2,
    "profile.default_content_setting_values.geolocation": 1,
    "profile.default_content_setting_values.notifications": 2
                                     })

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH, options = opt)
driver.get("https://www.houseofindya.com/zyra/hair-jewelry/cat?depth=3&label=Jewelry-Shop%20By%20Category-Hair%20Jewelry")
sleep(5)
#Finding number of items on the page
items = driver.find_elements_by_class_name("catgItem")
parentGUID = driver.current_window_handle
names = []
prices = []
description = []
#Processing all items by clicking on them
for i in range(len(items)):
    item = items[i]
    driver.execute_script("arguments[0].click();",item)
    sleep(6)
    allGUID = driver.window_handles
    #Switching to the opened tab to scrape data from there
    driver.switch_to.window(allGUID[1])
    #Closing pop up if it pops
    try:
        sleep(8)
        driver.find_element_by_class_name("CT_InterstitialClose").click()
    except:
        pass
    #Scraping data
    desc = driver.find_element_by_class_name("prodecbox.current")
    description.append(desc.text.replace("\n", " "))
    name = driver.find_element_by_xpath('//*[@id="wrapper"]/div[4]/div/div[2]/div[2]/h1')
    names.append(name.text)
    price = driver.find_element_by_xpath('//*[@id="wrapper"]/div[4]/div/div[2]/div[2]/h4/span[2]')
    prices.append(price.text)
    sleep(3)
    #CLosing the tab and switching back to main window
    driver.close()
    driver.switch_to.window(parentGUID)
    sleep(5)
    #Closing pop up if it pops on main page
    try:
        driver.find_element_by_class_name("closeload.header1pnlloadPopupcloseload").click()
    except:
        pass
    #Due to dynamic loading, items might have become "STALE", so we reinitialize it
    items = driver.find_elements_by_class_name("catgItem")

#print(description)
#Converting the data into a pandas dataframe and exporting it as a csv file.
di = {"Name": names, "Price(Rupees)": prices, "Description" : description}
df = pd.DataFrame(di)
df.to_csv("Hair-Jewelry_scraped", sep = '\t')
