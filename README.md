# Books Online SCRAPER

This app is a scraper of the website https://books.toscrape.com/


It allows you to get informations from books listed in different categories. It will produce one csv per book categories and list all books from that categories in it. It will also retrieve each image from each book.

The code will create two folders : one folder "csv" were it will store all csv created and one folder "media" were it will store all downloaded images.

The header of the csv is as follow : 

- product_page_url
- universal_product_code(upc)
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url


## Launching the app:

- First create a virtual environment.
- Install the depedencies using requirements.txt
- Run the app inside your virtual env with the command `python main.py`


## List of dependencies :
- beautifulsoup4==4.12.3
- certifi==2024.2.2
- charset-normalizer==3.3.2
- idna==3.6
- requests==2.31.0
- soupsieve==2.5
- wget==3.2