import requests
from bs4 import BeautifulSoup

startUrl = 'http://www.passwordrandom.com/most-popular-passwords/page/'
firstPage = 1
lastPage = 100

def main():
    f = open('common-passwords.txt', 'w')
    

    for currentPage in range(firstPage, lastPage):
        currentUrl = startUrl + str(currentPage)
        htmlResponse = requests.get(currentUrl)
        soup = BeautifulSoup(htmlResponse.content, 'html.parser')
        tableRows = soup.findAll('tr')
        for row in tableRows:
            children = row.findChildren()
            f.write(children[1].text + '\n')
        print(str(currentPage) + '/100')
        

if __name__ == '__main__':
    main()
