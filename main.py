'''main file for scraping amazon
-> writes price of book given to a csv file and compares to a previous value'''
import bs4
import requests
import csv
import datetime
import ezgmail
# sample text to find
# <span id="kindle-price" class="a-size-medium a-color-price"> $14.99 </span>  


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
        return 'N/A'


def update_price_csv(csv_location, urls):
    """updates prices for the csv"""
    with open(csv_location, 'a', newline='') as prices_file:
        file_writer = csv.writer(prices_file)
        current_date = str(datetime.date.today())
        file_writer.writerow([current_date] + url_helper(urls))


def check_for_price_difference(csv_location):
    """checks whether current price is different to previous price"""
    change = False
    text = ''
    with open(csv_location) as prices_file:
        file_reader = csv.reader(prices_file)
        file_reader_list = list(file_reader)
        for index, price in enumerate(file_reader_list[-1]):
            if index != 0 and len(file_reader_list[-2]) > index:
                if price != file_reader_list[-2][index]:
                    change = True
                    text += f'{file_reader_list[0][index]} is on sale for {price}\n'
    if not change:
        text = 'There is no price change'
        return change, text
    return change, text


def url_helper(urls):
    """Returns prices list for a list of given urls using list comprehension"""
    return [amazon_kindle_price_scraper(i) for i in urls]


def email_sender(email, text):
    """Sends an email to ..."""
    ezgmail.send(f'{email}', 'Book sale (Not spam)', text)

urls_location = r'C:\Users\o_dav\Dropbox\Hobby\amazon_webscrape\kindle-price-config-files\urls_file.txt'
csv_location = r'C:\Users\o_dav\Dropbox\Hobby\amazon_webscrape\kindle-price-config-files\daily_price_data.csv'
email_location = r'C:\Users\o_dav\Dropbox\Hobby\amazon_webscrape\kindle-price-config-files\email_file.txt'

with open(urls_location) as urls:
    url_list = urls.readlines()

with open(email_location) as emails:
    email = emails.readlines()[0]

if __name__ == '__main__':
    update_price_csv(csv_location, url_list)
    change, text = check_for_price_difference(csv_location)
    if change:
        email_sender(email, text)
    exit()