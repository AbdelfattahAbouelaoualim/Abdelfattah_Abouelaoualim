import requests
from bs4 import BeautifulSoup
import re

BASE = 'https://www.reuters.com/finance/stocks/financial-highlights/'
COMPANIES = ['AIR.PA', 'LVMH.PA', 'DANO.PA']

def get_sales_quarter(soup):
    try:
        my_soup = soup.find(class_="dataTable").find(class_="stripe").find_all("td", class_="data")
    except:
        raise Exception('Find soup failed!')
    print(f"Sales estimation: {my_soup[1].get_text()}")

def get_action_price(soup):
    try:
        action_price = soup.find('span',style='font-size: 23px;').text.strip()
    except:
        raise Exception('Get action price failed!')
    print(f"Action price: {action_price}")

def get_action_percent(soup):
    try:
        action_per = soup.find('span',class_='valueContentPercent').text.strip().replace("(", "").replace(")", "")
    except:
        raise Exception('Get action change percentage failed!')
    print(f"Action change percentage: {action_per}")

def get_share_owned(soup):
    try:
        share_owned = soup.find('strong',string='% Shares Owned:').findNext().text
    except:
        raise Exception('Get share owned failed!')
    print(f"Share owned: {share_owned}")

def get_dividend(soup):
    try:
        dividend = soup.find('td',string='Dividend Yield').parent()[1:]
    except:
        raise Exception('Get dividend failed!')
    print(f"Dividend yield: {dividend}")

if __name__ == '__main__':
    for c in COMPANIES:
        URL = BASE + c
        try:
            page = requests.get(URL)
        except:
            raise Exception('Get page failed!')

        soup = BeautifulSoup(page.content, 'html.parser')
        print(f"********** {c} ************")
        try:
            my_soup = soup.select("#content .sectionContent .sectionColumns .dataTable .stripe ")
        except:
            raise Exception('Get soup failed!')
        get_action_percent(soup)
        get_action_price(soup)
        get_sales_quarter(soup)
        get_dividend(soup)
        get_share_owned(soup)



