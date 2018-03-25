
import csv
import urllib.request
from bs4 import BeautifulSoup

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def parse(url):
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response)
    table = soup.find('table', class_='table')
    rows = table.find_all('tr')[1:]

    data = []
    i = 0
    for row in rows:
        cols = row.find_all('td')
        i = i + 1
        data.append({
            'Date': cols[0].text,
            'Open': cols[1].text,
            'High': cols[2].text,
            'Low': cols[3].text,
            'Close': cols[4].text,
            'Volume': cols[5].text,
            'Market Cap': cols[6].text
            })
    return data


def save(data, path):

    f = open(path, 'w')
    with f:
        fnames = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Market Cap']
        writer = csv.DictWriter(f, fieldnames=fnames, lineterminator='\n', delimiter=",")
        writer.writeheader()
        for line in data:
            writer.writerow(line)

BASE_URL = 'https://coinmarketcap.com/currencies/'
CURRENCY='ethereum'
URL_ADD='/historical-data/'
URL_START=20130428
URL_END=20180310
#BASE_URL = 'https://coinmarketcap.com/currencies/ethereum/historical-data/?start=20130428&end=20180309'

def main():
    CURRENCIES=('bitcoin','ethereum','cardano','eos','dash')

    for CURRENCY in CURRENCIES:
        data=parse(BASE_URL+CURRENCY+URL_ADD+'/?start='+str(URL_START)+'&end='+str(URL_END))
        filename=CURRENCY+'.csv'
        save(data, filename)

if __name__ == '__main__':
    main()