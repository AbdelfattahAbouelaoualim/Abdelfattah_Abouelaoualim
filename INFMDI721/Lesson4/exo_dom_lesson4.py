import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import multiprocessing as mp
import re

URL = "https://www.lacentrale.fr/listing?makesModelsCommercialNames=RENAULT%3AZOE&options=&page={page}&regions={region}"
EREA = ['FR-IDF', 'FR-PAC', 'FR-NAQ']
URL_BASE = 'https://www.lacentrale.fr'
URL_ARGUS = "https://www.lacentrale.fr/cote-auto-renault-zoe-{version}-{year}.html"
VERSIONS = {'LIFE', 'ZEN', 'INTENS', 'EDITION ONE', 'STAR WARS', 'TYPE 2'}

class lacentrale():

    def __int__(self, url = URL, erea = EREA, url_base = URL_BASE):
        self.url = url
        sel.erea = erea
        sel.url_base = url_base

    def give_me_soup(self, url):
        try:
            return BeautifulSoup(requests.get(url).text, "html.parser")
        except:
            raise Exception('Beurk... what this soup!')

    def pattern_urls(self, url):
        try:
            my_soup = self.give_me_soup(url)
        except:
            raise Exception('No, it\'s not my soup!')
        try:
            in_soup = my_soup.find_all("a", class_="linkAd ann")
        except:
            raise Exception('lacentrale changes its ingredients!')
        return list(map(lambda x: x.attrs['href'], in_soup))

    def urls(self, patterns, p, r):
        urls_ = (self.pattern_urls(URL.format(page=p, region=r)))
        for url in urls_:
            patterns.append(url)
        return patterns

    def pages_nbr(self, url):
        try:
            my_soup = self.give_me_soup(url)
        except:
            raise Exception('No, it\'s not my soup!')
        try:
            in_soup = my_soup.find("span", class_="numAnn")
        except:
            raise Exception('lacentrale changes its ingredients!')
        return int(np.ceil(int(in_soup.text)))

    def version(self, my_soup):
        try:
              in_soup = my_soup.find("div", class_="versionTxt txtGrey7C sizeC mB10 hiddenPhone")
        except:
            raise Exception('lacentrale changes its ingredients!')
        versions= set(in_soup.text.strip().upper())
        return VERSIONS.intersection(versions)


    def year(self, my_soup):
        return int(my_soup.find("span", class_="clearPhone lH35").text)

    def km(self, my_soup):
        return int("".join(re.findall(r"(\d+)", my_soup.find("span", class_="clearPhone lH40").text)))

    def price(self, my_soup):
        return int("".join(re.findall(r"(\d+)", my_soup.find("strong", class_="sizeD lH35 inlineBlock vMiddle ").text.strip())))

    def phone(self, my_soup):
        phone_s = my_soup.find("div", class_="phoneNumber1").text.strip()
        phone_ = re.findall(r"(\d+)", phone_s)
        phones = "".join(phone_)
        return phones if len(phones) <= 10 else phones[:11] + "/" + phones[11:]

    def seller(self, my_soup):
        return my_soup.find('div', class_='bold italic mB10').text.strip().split()[0]

    def info(self, url):
        my_soup = self.give_me_soup(URL_BASE + url)
        s = self.seller(my_soup)
        y = self.year(my_soup)
        k = self.km(my_soup)
        pr = self.price(my_soup)
        ph = self.phone(my_soup)
        return [s, y, k, pr, ph]

    def infos(self, a, u, erea):
        a[u] = self.info(u) + [erea]
        return a[u]

if __name__ == '__main__':
    c = lacentrale()
    erea_pages = {}
    urls_ = {}
    for erea in EREA:
        urll = URL.format(page = 1, region = erea)
        page_nbr = c.pages_nbr(urll)
        erea_pages[erea] = page_nbr
        jobs = []
        m = mp.Manager()
        u = m.list()
        for page in range(1, erea_pages[erea] + 1):
            p = mp.Process(target = c.urls, args = (u, page, erea))
            jobs.append(p)
            p.start()
        for p in jobs:
              p.join()
        urls_[erea] = list(u)


    m = mp.Manager()
    data = m.dict()
    jobs = []
    for erea in EREA:
        for u in urls_[erea]:
            p = mp.Process(target=c.infos, args=(data, u, erea))
            jobs.append(p)
            p.start()

    for p in jobs:
        p.join()

    data = dict(data)


    df = pd.DataFrame(data).transpose()
    df.rename(columns={0: "Seller", 1: "Year", 2: "Km",
                       3: "Price", 4: "Phone", 5: "Region"}, inplace=True)
    df.reset_index(drop=True, inplace=True)
    print("Sorted by ascending price...")
    print("----------------------------")
    print(df.sort_values("Price"))
