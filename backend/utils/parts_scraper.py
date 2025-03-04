import time
import json
import random
import re
from selenium import webdriver
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def get_driver():
    """Initialize and return an undetectable Selenium WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = uc.Chrome(use_subprocess=True, options=options)
    return driver


def clean_text(text):
    """Cleans extracted text by removing unnecessary content and normalizing spaces."""
    start_marker = "Get in touch, we're here to help!"
    end_marker = "Item is in stock and will ship today if your order is placed before 4:00 PM Eastern Standard Time."

    # Find the start position
    start_index = text.find(start_marker)
    if start_index != -1:
        text = text[start_index:]  # Keep text from start marker onwards

    # Find the end position
    end_index = text.find(end_marker)
    if end_index != -1:
        text = text[:end_index]

    text = text.encode("utf-8").decode("unicode_escape").encode("latin1").decode("utf-8")

    # Remove unwanted Unicode artifacts (e.g., "\u00XX", "\xXX")
    text = re.sub(r'\\u[0-9A-Fa-f]{4}|\\x[0-9A-Fa-f]{2}', '', text)
    
    # Normalize whitespace
    text = text.replace("\\n", "\n")  # Convert "\n" from string format to actual new lines
    text = re.sub(r'\s+', ' ', text)  # Reduce excessive whitespace
    text = re.sub(r'\n+', '\n', text)  # Ensure proper line breaks
    
    return text.strip()

def extract_all_text(page_url, driver):
    """Extracts and cleans text from a product page."""
    driver.get(page_url)
    time.sleep(random.uniform(5, 8))  # Allow page to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract visible text
    text = soup.get_text(separator=' ')
    text = clean_text(text)

    return text

# def extract_refrigerator_data(base_url, driver):
#     """Extracts refrigerator brand links, product types, individual product links, and product descriptions."""
#     driver.get(base_url)
#     time.sleep(random.uniform(5, 8))  # Allow page to load
#     soup = BeautifulSoup(driver.page_source, 'html.parser')

#     # Extract brand links
#     links = [a['href'] for a in soup.find_all('a', href=True)]
#     brand_links = [link for link in links if re.search(r'^/[A-Za-z0-9-]+-Refrigerator-Parts\.htm$', link)]

#     # Dictionaries for storing structured data
#     d1 = {}  # Brand name → Brand refrigerator product link
#     d2 = {}  # Brand refrigerator product link → Product types
#     d3 = {}  # Product type → Individual product links
#     d4 = {}  # Individual product link → Extracted text

#     # Iterate over each brand
#     for brand_link in brand_links[:1]:  # Test with 1 brand
#         brand_name = brand_link.split('-')[0].replace("/", "")
#         brand_url = f"https://www.partselect.com{brand_link}"
#         d1[brand_name] = brand_url

#         print(f"\nExtracting product categories for: {brand_name} ({brand_url})")

#         # Go to brand page and extract product types
#         driver.get(brand_url)
#         time.sleep(random.uniform(5, 8))
#         soup = BeautifulSoup(driver.page_source, 'html.parser')

#         links = [a['href'] for a in soup.find_all('a', href=True)]
#         product_type_links = [link for link in links if re.search(r'^/[A-Za-z0-9-]+-Refrigerator-[A-Za-z0-9-]+\.htm$', link)]
#         d2[brand_url] = product_type_links

#         # Print one product type for testing
#         if product_type_links:
#             print(f"  Sample product type link: {product_type_links[0]}")

#         # Iterate over each product type
#         for product_type_link in product_type_links[:1]:  # Test with 1 product type
#             product_type = product_type_link.split('-Refrigerator-')[1].replace('.htm', '').replace("-", " ")
#             product_url = f"https://www.partselect.com{product_type_link}"

#             print(f"    Extracting individual products for: {product_type} ({product_url})")

#             # Go to product type page and extract individual product links
#             driver.get(product_url)
#             time.sleep(random.uniform(5, 8))
#             soup = BeautifulSoup(driver.page_source, 'html.parser')

#             links = [a['href'] for a in soup.find_all('a', href=True)]
#             #individual_product_links = [link for link in links if re.search(r'^/PS\d+-[A-Za-z0-9-]+\.htm(\?.*)?$', link)]
#             cleaned_product_links = set()
#             for link in links:
#                 if re.search(r'^/PS\d+-[A-Za-z0-9-]+\.htm(\?.*)?$', link):
#                     base_link = link.split("#")[0]
#                     cleaned_product_links.add(base_link)
#             individual_product_links = list(cleaned_product_links)
#             d3[product_url] = individual_product_links

#             # Print one individual product link for testing
#             if individual_product_links:
#                 print(f"      Sample product link: {individual_product_links[0]}")

#             # Iterate over individual products
#             for product_link in individual_product_links[:3]:  # Test with 1 product
#                 product_page = f"https://www.partselect.com{product_link}"

#                 print(f"        Extracting text for product: {product_page}")

#                 # Extract and clean text from the product page
#                 product_text = extract_all_text(product_page, driver)
#                 d4[product_page] = product_text

#                 # Print a sample product text
#                 print("\n      Sample Product Text (truncated):")
#                 print(product_text[:500])  # Print first 500 characters for testing

#     return d1, d2, d3, d4

def extract_appliance_data(base_url, driver, category):
    """Extracts appliance brand links, product types, individual product links, and product descriptions."""
    driver.get(base_url)
    time.sleep(random.uniform(5, 8))  # Allow page to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract brand links
    links = [a['href'] for a in soup.find_all('a', href=True)]
    brand_links = [link for link in links if re.search(rf'^/[A-Za-z0-9-]+-{category}-Parts\.htm$', link)]

    # Dictionaries for storing structured data
    d1 = {}  # Brand name → Brand product page
    d2 = {}  # Brand product page → Product types
    d3 = {}  # Product type → Individual product links
    d4 = {}  # Individual product link → Extracted text

    # Iterate over each brand
    for brand_link in brand_links:  # Scrape one brand for testing
        brand_name = brand_link.split('-')[0].replace("/", "")
        brand_url = f"https://www.partselect.com{brand_link}"
        d1[brand_name] = brand_url

        print(f"\nExtracting product categories for {category}: {brand_name} ({brand_url})")

        # Go to brand page and extract product types
        driver.get(brand_url)
        time.sleep(random.uniform(5, 8))
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        links = [a['href'] for a in soup.find_all('a', href=True)]
        product_type_links = [link for link in links if re.search(rf'^/[A-Za-z0-9-]+-{category}-[A-Za-z0-9-]+\.htm$', link)]
        d2[brand_url] = product_type_links

        # Print one product type for testing
        if product_type_links:
            print(f"  Sample product type link: {product_type_links[0]}")

        # Iterate over each product type
        for product_type_link in product_type_links:  # Scrape one product type for testing
            product_type = product_type_link.split(f'-{category}-')[1].replace('.htm', '').replace("-", " ")
            product_url = f"https://www.partselect.com{product_type_link}"

            print(f"    Extracting individual products for: {product_type} ({product_url})")

            # Go to product type page and extract individual product links
            driver.get(product_url)
            time.sleep(random.uniform(5, 8))
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            links = [a['href'] for a in soup.find_all('a', href=True)]
            cleaned_product_links = set()
            for link in links:
                if re.search(r'^/PS\d+-[A-Za-z0-9-]+\.htm(\?.*)?$', link):
                    base_link = link.split("#")[0]
                    cleaned_product_links.add(base_link)
            individual_product_links = list(cleaned_product_links)
            d3[product_url] = individual_product_links

            # Print one individual product link for testing
            if individual_product_links:
                print(f"      Sample product link: {individual_product_links[0]}")

            # Iterate over individual products
            for product_link in individual_product_links:  # Scrape first 3 products for testing
                product_page = f"https://www.partselect.com{product_link}"

                print(f"        Extracting text for product: {product_page}")
                start_time = time.time()

                # Extract and clean text from the product page
                product_text = extract_all_text(product_page, driver)
                end_time = time.time()
                duration = end_time - start_time
                d4[product_page] = product_text

                print(f"Successfully scraped: {product_page} in {duration:.2f} seconds")

                # Print a sample product text
                print("\n      Sample Product Text (truncated):")
                print(product_text[:500])  # Print first 500 characters for testing

    return d1, d2, d3, d4
def main():
    driver = get_driver()
    try:
        categories = ["Refrigerator", "Dishwasher"]  # Scrape both
        all_data = {}

        for category in categories:
            base_url = f"https://www.partselect.com/{category}-Parts.htm"
            print(f"Starting {category} scraping...")

            d1, d2, d3, d4 = extract_appliance_data(base_url, driver, category)

            all_data[category] = {
                "Brand Links": d1,
                "Product Type Links": d2,
                "Individual Product Links": d3,
                "Product Descriptions": d4
            }

        with open("parts_data.txt", "a", encoding="utf-8") as f:
            f.write(json.dumps(all_data, indent=4))

    finally:
        driver.quit()
        print("Driver closed successfully.")
        print("Full Output saved to parts_data.txt")


if __name__ == "__main__":
    main()