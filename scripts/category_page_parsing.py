import requests
import csv
import os

from bs4 import BeautifulSoup
from scripts.product_page_parsing import product_parsing

def get_content(category_page_url):
    response = requests.get(category_page_url)
    if response.status_code != 200:
        print('\nERROR: Could not fetch category page')
        exit(1)
    return response

def get_urls(response):
    soup = BeautifulSoup(response.content, 'html.parser')

    urls_array = []
    pods = soup.find('ol', {'class': 'row'}).find_all('article', {'class': 'product_pod'})

    for pod in pods:
        links = pod.find_all('a', href=True)[0]
        urls_array.append(links['href'])

    return soup, urls_array

def next_page(soup):
    next = soup.find('li', {'class': 'next'})
    if next:
        next_page = next.find('a', href=True)
        next_url = next_page['href']
        return next_url

def category_parsing(website, category_page_url):
    #--------------------------------- GET PAGE -------------------------------------------
    response = get_content(category_page_url)
    soup, urls_array = get_urls(response)
    #--------------------------------------------------------------------------------------

    #----------------------------- WRITE CSV ----------------------------------------------
    category = soup.find('h1').text
    header = ['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
    books_arrays = []
    category_name = category.upper().replace(' ', '_')

    with open(f'./csv/{category_name}.csv', 'w+') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        next = "index.html"
        while next:
            suffix = "index.html"
            response = get_content(category_page_url.removesuffix(suffix) + next)
            soup, urls_array = get_urls(response)
            for url in urls_array:
                product_page_url = website + "catalogue" + url[8:]
                page_data = product_parsing(website, product_page_url)
                books_arrays.append(page_data)
            next = next_page(soup)
            if next:
                print("\n\nCONTINUE: continuing onto next page...")


        for array in books_arrays:
            writer.writerow(array)
    #---------------------------------------------------------------------------------------
    