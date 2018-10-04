from urllib2 import urlopen
from bs4 import BeautifulSoup as soup
from twilio.rest import Client
import time
import csv
import json

twilioNumber = "(786) 724-2238"
account_sid = "AC384f63e594bd6c222ac8e9b00a0d2e8a"
auth_token = "8f02917112007c347acf2940b59122f3"
dbFile = "db.csv"
fieldnames = ['title', 'price', 'postTime', 'url', 'id']
baseUrl = "https://offerup.com/search/?"

def getSearchUrls():
    urls = []
    with open("config.json", "r") as config:
        data = json.load(config)
        for search in data:
            url = baseUrl
            for term in search:
                url += "{0}={1}&".format(term, search[term])
            urls.append(url[:-1])
    config.close()
    return urls

def writeDb(lines):
    with open("db.csv", "a") as dbCsv:
        db = csv.DictWriter(dbCsv, fieldnames=fieldnames)
        db.writeheader()
        db.writerow(lines)
    dbCsv.close()


def readDb():
    data = []
    with open("db.csv", "r") as dbCsv:
        db = csv.DictReader(dbCsv)
        for line in db:
            data.append(line)
        dbCsv.close()
        return data


def findall_lookup(url, tag, elem='', val=''):
    time.sleep(1)
    uClient = urlopen(url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    if val != '' or elem != '':
        return page_soup.findAll(tag, {elem: val})
    else:
        return page_soup.findAll(tag)


class formatCard():

    def __init__(self, card):
        self.contents = card.div.contents
        self.title = self.contents[1].contents[0].string
        self.price = self.contents[1].contents[1].div.string
        self.url = "https://offerup.com" + card['href']
        self.id = card['href']
        self.postTime = 0

    def getpostTime(self):
        page = findall_lookup(self.url, "span", "class", "_147ao2d8")
        elem = page[0].contents[2]
        str = elem.string
        self.postTime = str
        return str

    def sendMessage(self, client):
        message = client.messages.create(
            to="+15615960343",
            from_=twilioNumber,
            body=self.title + "\n" + self.price + "\n" + self.url + "\n"
        )
        return message.sid

    def toDict(self):
        return {
            'title': self.title,
            'price': self.price,
            'postTime': self.postTime,
            'url': self.url,
            'id': self.id
        }


urls = getSearchUrls()
id = "db-item-list"
client = Client(account_sid, auth_token)
dbDict = readDb()
db = {}

if len(dbDict) > 1:
    for card in dbDict:
        db[card['id']] = {'price': card['price'], 'postTime': card['postTime'], 'url': card['url'],'title': card['title']}

for url in urls:
    html = findall_lookup(url, "a", "class", "_109rpto db-item-tile")
    for i in html:
        card = formatCard(i)
        if card.price == 'SOLD':
            continue
        postTime = card.getpostTime()
        if card.id in db:
            continue
        writeDb(card.toDict())
        print card.url
        print postTime
        print card.title
        print card.price
        # sid = card.sendMessage(client)
        # print sid + "\n"
