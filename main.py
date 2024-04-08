import requests
import os

from bs4 import BeautifulSoup

from scripts.category_page_parsing import category_parsing


print("INIT: Initializing process...")


#------------------------- CHECK FOR DIRECTORIES -----------------------------------------
print("INIT: Check or create relevant directories...")
dir_exists = os.path.exists("csv/")
if not dir_exists:
    os.makedirs("csv/")

dir_exists = os.path.exists("media/")
if not dir_exists:
    os.makedirs("media/")
#--------------------------------------------------------------------------------------


#------------------------------ GET MAIN PAGE -----------------------------------------
print("INIT: Get main page...")
main_page = "https://books.toscrape.com/index.html"
response = requests.get(main_page)
if response.status_code != 200:
    print('ERROR: Could not fetch main page.')
    exit(1)
print("\nSUCCESS: Successfully fetched main page.")
#--------------------------------------------------------------------------------------


#----------------------------- GET ALL CATEGORIES URLS --------------------------------
soup = BeautifulSoup(response.content, 'html.parser')

categories = soup.find('div', {'class': "side_categories"}).findChild('ul', recursive=False).findChild('li', recursive=False).findChild('ul', recursive=False).find_all('li')
#--------------------------------------------------------------------------------------


#---------------- PARSE PRODUCTS FOR EACH PAGE OF EACH CATEGORY -----------------------
for category in categories:
    category_name = category.find('a').text.strip()
    print(f"\nSTART: Start importing products for category {category_name}...")
    path = category.find('a', href=True)
    category_page_url = "https://books.toscrape.com/" + path['href']

    is_next = category_parsing(category_page_url, False)
    while is_next:
        print("\nCONTINUE: continuing onto next page...")
        suffix = "index.html"
        is_next = category_parsing(category_page_url.removesuffix(suffix) + is_next, True)
#--------------------------------------------------------------------------------------


print("END: All CSV are created.")
