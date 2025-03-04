import time
import json
import random
import re
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
import traceback
import os
from selenium import webdriver
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

#SCRAPER WITH POOLING FOR FASTER 
#First use other scraper then this one
def get_driver():
    """Initialize and return an undetectable Selenium WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    driver = uc.Chrome(use_subprocess=True, options=options)
    return driver
def clean_text(text):
    """Cleans extracted text by removing unnecessary content and normalizing spaces."""
    start_marker = "Get in touch, we're here to help!"
    end_marker = "Item is in stock and will ship today if your order is placed before 4:00 PM Eastern Standard Time."

    start_index = text.find(start_marker)
    if start_index != -1:
        text = text[start_index:]

    end_index = text.find(end_marker)
    if end_index != -1:
        text = text[:end_index]

    text = text.encode("utf-8").decode("unicode_escape").encode("latin1").decode("utf-8")
    text = re.sub(r"\\u[0-9A-Fa-f]{4}|\\x[0-9A-Fa-f]{2}", "", text)
    text = text.replace("\\n", "\n")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\n+", "\n", text)

    return text.strip()

def extract_all_text(page_url, driver):
    """Extracts and cleans text from a product page."""
    driver.get(page_url)
    time.sleep(random.uniform(5, 8))  
    soup = BeautifulSoup(driver.page_source, "html.parser")

    text = soup.get_text(separator=" ")
    return clean_text(text)


def process_brand(brand_data):
    """Processes all product types and products for a given brand"""
    brand_name, brand_url, category = brand_data
    driver = get_driver()
    brand_results = {}

    try:
        driver.get(brand_url)
        time.sleep(random.uniform(1, 2))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        product_type_links = [
            link["href"]
            for link in soup.find_all("a", href=True)
            if re.search(rf"^/[A-Za-z0-9-]+-{category}-[A-Za-z0-9-]+\.htm$", link["href"])
        ]
        
        product_data = {}
        for product_type_link in product_type_links:
            product_type = product_type_link.split(f"-{category}-")[1].replace(".htm", "").replace("-", " ")
            product_url = f"https://www.partselect.com{product_type_link}"
            
            driver.get(product_url)
            time.sleep(random.uniform(1, 2))
            soup = BeautifulSoup(driver.page_source, "html.parser")
            individual_product_links = list(
                set(
                    link.split("#")[0]
                    for link in [a["href"] for a in soup.find_all("a", href=True)]
                    if re.search(r"^/PS\d+-[A-Za-z0-9-]+\.htm(\?.*)?$", link)
                )
            )
            
            product_descriptions = {}
            for product_link in individual_product_links:  
                product_page = f"https://www.partselect.com{product_link}"
                product_text = extract_all_text(product_page, driver)
                product_descriptions[product_page] = product_text
            
            product_data[product_url] = product_descriptions
        
        brand_results[brand_name] = product_data
    
    finally:
        driver.quit()
    
    with open(f"{category}_{brand_name}_data.json", "w", encoding="utf-8") as f:
        json.dump(brand_results, f, indent=4)
    
    print(f"Finished processing {brand_name}")



def scrape_all_brands(category):
    """Scrapes all brands for the given category until all links are processed."""
    driver = get_driver()
    base_url = f"https://www.partselect.com/{category}-Parts.htm"

    driver.get(base_url)
    time.sleep(random.uniform(1, 2))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    brand_links = [
        [link.split("-")[0].replace("/", ""), f"https://www.partselect.com{link}", category]
        for link in [a["href"] for a in soup.find_all("a", href=True)]
        if re.search(rf"^/[A-Za-z0-9-]+-{category}-Parts\.htm$", link)
    ]

    driver.quit()

    print(f"Found {len(brand_links)} brands for {category}")

    #Parallel Pool 
    with ThreadPoolExecutor(max_workers=4) as executor:
        try:
            results = list(executor.map(process_brand, brand_links))
        except Exception as e:
            print(f"Error in processing pool: {e}")
            traceback.print_exc()


if __name__ == "__main__":
    categories = ["Refrigerator", "Dishwasher"]  
    
    for category in categories:
        scrape_all_brands(category)
    
    print("Scraping completed for all categories!")
