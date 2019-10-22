# Date: 01/02/2019
# Author: Mohamed
# Description: Search for links

import requests
from queue import Queue
from bs4 import BeautifulSoup as bs


class Search(object):

    def __init__(self, dork):
        self.is_alive = True
        self.links = Queue()
        self.url = 'http://www.search-results.com/web?q={0}&page='.format(dork)

    def find_links(self):
        page = 0
        while self.is_alive:
            page += 1
            url = self.url + str(page)

            html = requests.get(url).content

            try:
                for a in bs(html, 'html.parser').find('section', {'id': 'algo-container'}).find_all('a', href=True):
                    link = a['href']

                    if '=' in link:
                        self.links.put(link)

            except:
                self.is_alive = False

    def get_link(self):
        if self.links.qsize():
            return self.links.get()

    def start(self):
        self.find_links()

    def stop(self):
        self.is_alive = False
