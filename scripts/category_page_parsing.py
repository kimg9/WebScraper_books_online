import requests
import csv
import os

from bs4 import BeautifulSoup
from product_page_parsing import product_parsing

def next_page(soup):
    next = soup.find('li', {'class': 'next'})
    if next:
        next_page = next.find('a', href=True)
        next_url = next_page['href']
        return next_url
    else:
        return False

def category_parsing(category_page_url, is_next):
    #--------------------------------- GET PAGE -------------------------------------------
    response = requests.get(category_page_url)
    if response.status_code != 200:
        print('Could not fetch the page')
        exit(1)
    #--------------------------------------------------------------------------------------


    #----------------------------- GET PRODUCT PAGES URLS ---------------------------------
    soup = BeautifulSoup(response.content, 'html.parser')

    urls_array = []
    pods = soup.find('ol', {'class': 'row'}).find_all('article', {'class': 'product_pod'})

    for pod in pods:
        links = pod.find_all('a', href=True)[0]
        urls_array.append(links['href'])
    #--------------------------------------------------------------------------------------


    #------------------------- CHECK FOR DIRECTORY -----------------------------------------
    is_exist = os.path.exists("csv/")
    if not is_exist:
        os.makedirs("csv/")
    #--------------------------------------------------------------------------------------


    #----------------------------- WRITE CSV ----------------------------------------------
    category = soup.find('h1').text
    header = ['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']

    # CASE 2: is a following page ------------------------------------------------------------
    if is_next:
        with open(f'./csv/{category}_products.csv', 'a') as file:
            writer = csv.writer(file)
            for url in urls_array:
                product_page_url = "https://books.toscrape.com/catalogue" + url[8:]
                data = product_parsing(product_page_url)
                writer.writerow(data)
        file.close()
        return(next_page(soup))
    else:
    # CASE 1: is a first page --------------------------------------------------------------
        with open(f'./csv/{category}_products.csv', 'w+') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for url in urls_array:
                product_page_url = "https://books.toscrape.com/catalogue" + url[8:]
                data = product_parsing(product_page_url)
                writer.writerow(data)
        file.close()
        return(next_page(soup))
    #---------------------------------------------------------------------------------------
    