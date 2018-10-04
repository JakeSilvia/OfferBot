from twilio.rest import Client
import Network
import csv
import Card
import os

twilioNumber = "(786) 724-2238"
account_sid = "AC384f63e594bd6c222ac8e9b00a0d2e8a"
auth_token = "8f02917112007c347acf2940b59122f3"
dbFile = "db.csv"
fieldnames = ['title', 'price', 'postTime', 'url', 'id']
baseUrl = "https://offerup.com/search/?"

def writeDb(lines):
    exists = os.path.isfile(dbFile)
    with open(dbFile, "a") as dbCsv:
        db = csv.DictWriter(dbCsv, fieldnames=fieldnames)
        if not exists:
            db.writeheader()

        db.writerow(lines)
    dbCsv.close()


def readDb():
    data = []
    with open(dbFile, "r") as dbCsv:
        db = csv.DictReader(dbCsv)
        for line in db:
            data.append(line)
        dbCsv.close()
        return data

urls = Network.getSearchUrls(baseUrl)
id = "db-item-list"
client = Client(account_sid, auth_token)
dbDict = readDb()
db = {}

if len(dbDict) > 1:
    for card in dbDict:
        db[card['id']] = {'price': card['price'], 'postTime': card['postTime'], 'url': card['url'],'title': card['title']}

for url in urls:
    html = Network.findall_lookup(url, "a", "class", "_109rpto db-item-tile")
    print("Finding cards")
    for i in html:
        card = Card.NewCard(i)
        if card.err is not None:
            print("error: ", card.err)
            continue
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
