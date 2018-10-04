import json
import time
from urllib2 import urlopen
from bs4 import BeautifulSoup as soup

def getSearchUrls(baseUrl):
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
