from selenium import webdriver
from bs4 import BeautifulSoup
import re
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
import json
import pandas as pd
from selenium.webdriver.chrome.service import Service



def tokopedia_scrape(katakunci):
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('log-level=2')
    # chrome_options.add_argument('headless')
    s = Service("./chromedriver")
    driver = webdriver.Chrome(service=s, options=chrome_options)
    links = []
    
    url = f"https://www.tokopedia.com/{katakunci}/product"
    # url = 'https://shopee.co.id/search?keyword=' + katakunci
    try:
        photo_product, name_product, price_product, product_desc = list(), list(), list(), list()
        ds = []
        s = list()
        driver.get(url)
        time.sleep(5)
        driver.execute_script('window.scrollTo(0, 1500);')
        time.sleep(5)
        driver.execute_script('window.scrollTo(0, 2500);')
        time.sleep(5)
        soup_a = BeautifulSoup(driver.page_source, 'html.parser')
        for i in driver.find_elements_by_css_selector("div[class='css-1f2quy8']>a"):
            ds.append(i.get_attribute("href"))
        print(ds)
        for i in range(len(ds)):
            # open another URL on one tab
            driver.switch_to.window(driver.window_handles[0])
            driver.get(ds[i])
            time.sleep(2)
#             driver.execute_script('window.scrollTo(0, 1500);')
#             time.sleep(5)
#             driver.execute_script('window.scrollTo(0, 2500);')
            product_name = driver.find_element(By.XPATH, "//h1[contains(@class, 'css-t9du53')]").text
            product_price = driver.find_element(By.XPATH,"//div[contains(@class, 'price')]").text
            product_description = driver.find_element(By.XPATH, "//div[contains(@data-testid, 'lblPDPDescriptionProduk')]").text
            name_product.append(product_name), price_product.append(product_price.replace("Rp","")), product_desc.append(product_description.replace("\n", " "))

        dict= {
            "product_name":name_product,
            "product_price": price_product,
            "product_description": product_desc,
        }
        print(dict)
        df = pd.DataFrame(dict, columns=["Product Photo", "Product Name", "Product Price", "Product Description"])
        df.to_csv("tokopedia_product.csv", index=False)
        
        driver.quit()
            
            
            
    except TimeoutException:
        print('failed to get links with query ')
        driver.quit()
    return links


