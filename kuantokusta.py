import requests
from bs4 import BeautifulSoup
import time

f = open('test.txt', 'w')

start = time.time()
offersScraped = 0
itemsScraped = 0


pages = []
offers = []
baseSearchLink = 'https://www.kuantokusta.pt/search?q='
userQuery = raw_input('Query:  \n')
baseSearchLink += userQuery
htmlResponse = requests.get(baseSearchLink);
soup = BeautifulSoup(htmlResponse.content, 'html.parser');

items = soup.findAll('a', {'class':'product-item-name'})

for item in items:
    title = item.get('title')
    url = 'https://kuantokusta.pt'+item.get('href')
    itemPage = {'itemTitle':title, 'pageUrl':url}
    pages.append(itemPage)
    itemsScraped+=1

for page in pages:
    htmlResponse = requests.get(page["pageUrl"]);
    soup = BeautifulSoup(htmlResponse.content, 'html.parser');
    storeLines = soup.findAll('div',{'class':'store-line'})
    for storeLine in storeLines:
        sellers = storeLine.findAll('meta', {'itemprop':'name'})
        for seller in sellers:
            offer = {
                'itemName':page['itemTitle'],
                'itemPrice':storeLine.get('data-price'),
                'store':seller.get('content')
            }
            offers.append(offer)
            f.write((str(offer) + '\n').encode('UTF-8')) 
            offersScraped+=1
f.close()

end = time.time()

elapsed = end - start

print("Scraped {} store offers in {} seconds. Total of {} items.".format(offersScraped, round(elapsed, 2), itemsScraped))
