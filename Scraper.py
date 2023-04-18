from datetime import datetime
import psycopg2
import requests
from bs4 import BeautifulSoup
import sqlalchemy
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *

import Database


def each_page(url):
    response = requests.get(url)
    current_page = url.split('=')[-1]
    print("Stranica: ", url)
    soup = BeautifulSoup(response.text, 'html.parser')
    ads = soup.find_all('li', {'class': 'product-single-item'})

    if len(ads) > 0:
        seen_titles = []  # lista za praćenje naslova oglasa koje smo već ispisali
        for ad in ads:

            title = ad.find('h3', {'class': 'product-title'}).text.strip()
            if title in seen_titles:  # preskačemo ispis ako smo već ispisali oglas sa ovim naslovom
                continue
            seen_titles.append(title)  # dodajemo naslov oglasa u listu viđenih naslova

            price = ad.find('p', {'class': 'product-price'}).text.strip()
            posted = ad.find('time', {'class': 'pin-item'}).text.strip()
            mesto = ad.find('div', {'class': 'pin-item'})
            mesto = mesto.text.strip() if mesto is not None else ''
            link = 'https://sasomange.rs'+ad.find('a', {'class': 'product-link'})['href']

            ul_tag = soup.find('ul', {'class': 'highlighted-attributes'})
            span_tags = ul_tag.find_all('span')
            oglas = [title, mesto, price, posted[0:-1], link]
            for span in span_tags:
                oglas.append(span.text.strip())

            for i in range(len(oglas)):
                if len(oglas)==12:
                    oglas[i] = oglas[i].replace('\xa0€', '').replace('cm³', '').replace('km', '').replace(' kW','').replace('KS','').replace(' ', '')
            print(oglas)
            Database.add_oglas(oglas[0],oglas[1],int(oglas[2].replace('.','').replace('Dogovor',"0").replace('Kontakt',"0").replace('Naupit',"0")),datetime.strptime(oglas[3], '%d.%m.%Y').date(),oglas[4],oglas[5],oglas[6],oglas[7],int(oglas[8]),int(oglas[9]),int(oglas[10]),int(oglas[11]))
        print("Podaci uneti u bazu!")

    else: return []


page=0
info=True
while page<50:
    if each_page('https://sasomange.rs/c/polovni-automobili?currentPage={}'.format(page))==[]:
        print("Na sajtu nema vise oglasa.")
        break
    else:
        print("")
        page = page + 1
