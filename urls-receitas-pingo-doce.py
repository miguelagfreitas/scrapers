import requests
from bs4 import BeautifulSoup
import time
import json

f = open('urls.dat', 'w')

recipeUrls = []
page = 1

while True:
    searchUrl = 'https://www.pingodoce.pt/wp-content/themes/pingodoce/ajax/pd-ajax.php?type=recipe&page='+str(page)+'&query=&filters=&action=custom-search'
    htmlResponse = requests.get(searchUrl)
    responseHTML = json.loads(htmlResponse.text)
    soup = BeautifulSoup(responseHTML['data']['html'], 'html.parser')
    cardRecipes = soup.findAll('a', {'class': 'pd-card recipe'})
    if(len(cardRecipes) == 0):
        break
    for cardRecipe in cardRecipes:
        recipeUrls.append(cardRecipe.get('href'))
        print cardRecipe.get('href')
        f.write(cardRecipe.get('href') + '\n')
    page += 1
f.close()

print("Scraped {} recipe links.".format(len(recipeUrls)))
