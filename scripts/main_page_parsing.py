import requests
import os

from bs4 import BeautifulSoup

from scripts.category_page_parsing import category_parsing


#------------------------- CHECK FOR DIRECTORIES -----------------------------------------
def init():
    print("INIT: Check or create relevant directories...")
    dir_exists = os.path.exists("csv/")
    if not dir_exists:
        os.makedirs("csv/")

    dir_exists = os.path.exists("media/")
    if not dir_exists:
        os.makedirs("media/")
#--------------------------------------------------------------------------------------

#------------------------------ GET MAIN PAGE -----------------------------------------
def get_main_page(website):
    print("INIT: Get main page...")
    main_page = website + "index.html"
    response = requests.get(main_page)
    if response.status_code != 200:
        print('ERROR: Could not fetch main page.')
        exit(1)
    print("\nSUCCESS: Successfully fetched main page.")
    return response
#--------------------------------------------------------------------------------------

#---------------- PARSE PRODUCTS FOR EACH PAGE OF EACH CATEGORY -----------------------
def parse(response, website):
    soup = BeautifulSoup(response.content, 'html.parser')

    categories = soup.find('div', {'class': "side_categories"}).findChild('ul', recursive=False).findChild('li', recursive=False).findChild('ul', recursive=False).find_all('li')

    for category in categories:
        category_name = category.find('a').text.strip()
        print(f"\nSTART: Start importing products for category {category_name}...")
        path = category.find('a', href=True)
        category_page_url = website + path['href']
        category_parsing(website, category_page_url)
#--------------------------------------------------------------------------------------

def main():
    website = "https://books.toscrape.com/"
    print("INIT: Initializing scarping process...")
    init()
    response = get_main_page(website)
    parse(response, website)
    print("END: All CSV are created.")

if __name__ == "__main__":
    main()



