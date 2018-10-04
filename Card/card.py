import Network

class NewCard():

    def __init__(self, card):
        try:
            self.contents = card.div.contents
            self.title = _validate(self.contents[1].contents[0])
            self.price = _validate(self.contents[1].contents[1].span)
            self.url = _validate("https://offerup.com" + card['href'])
            self.id = _validate(card['href'])
            self.postTime = 0
            self.err = None
        except Exception as e:
            self.err = e

    def getpostTime(self):
        page = Network.findall_lookup(self.url, "span", "class", "_147ao2d8")
        elem = page[0].contents[2]
        str = elem.string
        self.postTime = str
        return str

    def sendMessage(self, client, phone):
        message = client.messages.create(
            to="+15615960343",
            from_=phone,
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

def _validate(item):
    try:
        item = item.string
    except AttributeError:
        pass

    try:
        item = item.encode("utf-8")
    except:
        pass

    return item