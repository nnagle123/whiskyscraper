import requests
from bs4 import BeautifulSoup
import pandas as pd



baseurl = 'https://www.thewhiskyexchange.com/'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    
productlinks = []

for x in range(1,6):
    r = requests.get(f'https://www.thewhiskyexchange.com/c/35/japanese-whisky?pg={x}#productlist-filter')
    soup = BeautifulSoup(r.content, features='lxml')

    productlist = soup.find_all('div', class_='item')

    for item in productlist:
        for link in item.find_all('a', href=True):
            productlinks.append(baseurl + link['href'])


# testlink = 'https://www.thewhiskyexchange.com/p/25880/hanyu-1985-the-joker-monochrome-label'
whiskylist = []
for link in productlinks:
    r = requests.get(link, headers = headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    name = soup.find('h1', class_='product-main__name').text.strip()
    price = soup.find('p', class_='product-action__price').text.strip()    
    try:
        rating = soup.find('div', class_="review-overview").text.strip()
    except:
        rating = 'no rating'


    whisky = {
        'name': name,
        'rating': rating,
        'price': price
    }

    whiskylist.append(whisky)
    print('Saving: ', whisky['name'])

df = pd.DataFrame(whiskylist)
print(df.head(35))