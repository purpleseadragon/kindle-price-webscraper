'''main file for scraping amazon
-> writes price of book given to a csv file and compares to a previous value
emails if different to previous'''
import bs4
import requests
import csv
import datetime

print('testing...')
# sample text to find
#  <span id="kindle-price" class="a-size-medium a-color-price"> $14.99 </span>  


def amazon_kindle_price_scraper(url):
    """Returns price of book of kindle book from amazon page"""
    # obtains html using requests
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}
    res = requests.get(url, headers=headers)
    res.raise_for_status()

    # creation of soup object and parsing of html
    amazon_soup = bs4.BeautifulSoup(res.text, 'html.parser')
    all_spans = amazon_soup.find_all('span')
    for element in all_spans:
        if element.get('id') == "kindle-price" and element.get('class') == ['a-size-medium', 'a-color-price']:
            price = element.contents
        # print(f"id   : {element.get('id')}")
        # print(f"class: {element.get('class')}")

    try:
        price = price[0]
        price = price.strip()
        return price
    except UnboundLocalError:
        print('A valid price was not found, perhaps the website given is incorrect.')


def update_price_csv():
    """updates prices for the csv"""
    with open('daily_price_data.csv') as prices_file:
        file_reader = csv.reader(prices_file)
        print(list(file_reader)) 
    return


url1 = 'https://www.amazon.com.au/Gardens-Moon-Malazan-Book-Fallen-ebook/dp/B0031RS64G/ref=sr_1_3?crid=1R4P3V5X90EJS&keywords=gardens+of+the+moon&qid=1640488583& \
    s=digital-text&sprefix=%2Cdigital-text%2C591&sr=1-3'
url2 = 'https://www.amazon.com.au/Deadhouse-Gates-Malazan-Book-Fallen-ebook/dp/B0031RS6PU'
url3 = 'https://www.amazon.com.au/Wintersteel-Cradle-Book-Will-Wight-ebook/dp/B08JMF22F2'

if __name__ == '__main__':
    # print(amazon_kindle_price_scraper(url1))
    # print(amazon_kindle_price_scraper(url2))
    # print(amazon_kindle_price_scraper(url3))
    update_price_csv()