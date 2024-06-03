import requests
from bs4 import BeautifulSoup
import os
import wget 
import csv


class OnlineData():
    def __init__(self, url, website):
        self.url = url
        self.website = website

    suffix = "index.html"
    soup = BeautifulSoup(features="html.parser")

    def get_html_content(self):
        # print(self.url)
        response = requests.get(self.url)
        if response.status_code != 200:
            print('\nERROR: Could not fetch page')
            exit(1)
        self.soup = BeautifulSoup(response.content, 'html.parser')


class SavedObject():
    @staticmethod
    def check_directory(path):
        directory_exists = os.path.exists(path)
        if not directory_exists:
            os.makedirs(path)


class Book(OnlineData, SavedObject):
    upc = ""
    title = ""
    price_with_tax = ""
    price_without_tax = ""
    number_available = ""
    product_description = ""
    category = ""
    review_rating = ""
    image_url = ""

    def load_data(self):
        self.get_html_content()
        self.category = self.soup.find('ul', {'class': 'breadcrumb'}).find_all('li')[2].text.strip()
        self.title = self.soup.find('article', {'class': 'product_page'}).findChild("h1").text.strip()

        try:
            self.product_description = self.soup.find('article', {'class': 'product_page'}).findChild('p', recursive=False).text
        except AttributeError:
            self.product_description = ""

        info_table = self.soup.find('article', {'class': 'product_page'}).findChild('table', recursive=False).find_all('td')
        self.upc = info_table[0].text
        self.price_without_tax = info_table[2].text
        self.price_with_tax = info_table[3].text
        self.number_available = "".join(_ for _ in info_table[5].text if _ in "0123456789")

        review_rating = self.soup.find('article', {'class': 'product_page'}).find('div', {'class': 'row'}).find('div', {'class': 'product_main'}).findChildren('p', recursive=False)[2]['class']
        if "One" in review_rating:
            self.review_rating = "1"
        elif "Two" in review_rating:
            self.review_rating = "2"
        elif "Three" in review_rating:
            self.review_rating = "3"
        elif "Four" in review_rating:
            self.review_rating = "4"
        elif "Five" in review_rating:
            self.review_rating = "5"

    def get_image(self):
        self.load_data()
        self.image_url = self.website + (self.soup.find('article', {'class': 'product_page'}).find('div', {'class': 'item active'}).findChild('img', recursive=False)['src'][6:])
        image_extension = os.path.splitext(self.image_url)[1]
        path = (f"media/{self.category.upper().replace(' ', '_')}/")
        self.check_directory(path)
        print(f"\nIMAGE: downloading image for book {self.title}...")
        for ch in ['\\','`','*','/','{','}','[',']','(',')','>','#','+','-','.','!','?','$','\'',',',' ','!',':']:
            if ch in self.title:
                self.title = self.title.lower().replace(ch, '_')
        image_path = path + self.category.upper().replace(' ', '_') + "_" + self.title
        file_exists = os.path.exists(image_path)
        if file_exists:
            os.remove(image_path)
        wget.download(self.image_url, out = (image_path + image_extension))      


class Category(OnlineData):
    urls_array = []
    books_array = [Book]
    category_url = ""
    next_url = "index.html"
    name = ""

    def load_data(self):
        self.get_html_content()
        self.name = self.soup.find('h1').text.upper().replace(' ', '_')

    def get_urls(self):
        self.urls_array = []
        self.load_data()
        pods = self.soup.find('ol', {'class': 'row'}).find_all('article', {'class': 'product_pod'})
        for pod in pods:
            links = pod.find_all('a', href=True)[0]
            self.urls_array.append(links['href'])

    def next_page(self):
        next = self.soup.find('li', {'class': 'next'})
        if next:
            next_page = next.find('a', href=True)
            self.url = self.category_url + next_page['href']
            return True
        return False
        
    def data_collection_logic(self):
        self.get_urls()
        for url in self.urls_array:
            book = Book(self.url, self.website)
            book.url = self.website + "catalogue" + url[8:]
            book.get_image()
            self.books_array.append(book)
        next = self.next_page()
        return next
        
    def create_csv(self):
        header = ['url', 'upc', 'title', 'price_with_tax', 'price_without_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
        self.name = self.name.upper().replace(' ', '_')
        with open(f'./csv/{self.name}.csv', 'w+') as file:
            writer = csv.DictWriter(file,fieldnames=header,extrasaction='ignore')
            writer.writeheader()
            next = "index.html"
            self.category_url = self.url.removesuffix(self.suffix)
            while next:
                next = self.data_collection_logic()
                if next:
                    print("\n\nCONTINUE: continuing onto next page...")
            for book in self.books_array:
                writer.writerow({k:getattr(book, k) for k in vars(book)})


class Website(OnlineData, SavedObject):
    def __init__(self, url):
        self.url = url

    def begin(self):
        print("INIT: Check or create relevant directories...")
        self.check_directory("csv/")
        self.check_directory("media/")

    def get_main_page(self):
        print("INIT: Get main page...")
        self.url += self.suffix
        self.get_html_content()
        print("\nSUCCESS: Successfully fetched main page.")

    def load_data(self):
        self.begin()
        self.get_main_page()
        categories = self.soup.find('div', {'class': "side_categories"}).findChild('ul', recursive=False).findChild('li', recursive=False).findChild('ul', recursive=False).find_all('li')

        for category in categories:
            path = category.find('a', href=True)
            name = category.find('a').text.strip()
            self.url = self.url.removesuffix(self.suffix)
            category = Category(self.url + path['href'], self.url)
            category.name = name
            print(f"\nSTART: Start importing products for category {category.name}...")
            category.create_csv()