#!/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import pandas as pd

# on cherche le PC avec la remise la plus intéressante sur Darty et rue du commerce

url_daty_lenovo = "https://www.darty.com/nav/extra/list?s=def&c=1655080&cat=756"
url_daty_acer = "https://www.darty.com/nav/extra/list?s=def&c=1655074&cat=756"
url_rueducommerce_lenovo = "https://www.rueducommerce.fr/rayon/ordinateurs-64/ordinateur-portable-657?sort=expert&view=grid&marque=lenovo"
url_rueducommerce_acer = "https://www.rueducommerce.fr/rayon/ordinateurs-64/ordinateur-portable-657?sort=expert&view=grid&marque=acer"

all_url = {"darty": [url_daty_lenovo, url_daty_acer], "rueducommerce": [url_rueducommerce_lenovo, url_rueducommerce_acer]}


remise_dict_darty = {"lenovo": [], "acer": []}
remise_list_darty = {"lenovo": 0, "acer": 0}
for url in all_url['darty']:
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    remises = soup.find_all('div', class_='rouge')
    url_find = url.find("1655080")
    for remise in remises:
        if url_find != -1:
            remise_dict_darty["lenovo"].append(int(remise.find('span', {'class','striped_price'}).text.strip().split('%')[0].split(' ')[1]))
        else:
            remise_dict_darty["acer"].append(int(remise.find('span', {'class','striped_price'}).text.strip().split('%')[0].split(' ')[1]))

    if url_find != -1:
        remise_list_darty["lenovo"] = max(remise_dict_darty["lenovo"])
    else:
        remise_list_darty["acer"] = max(remise_dict_darty["acer"])

print(remise_list_darty)

