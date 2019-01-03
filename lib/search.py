# Date: 01/02/2019
# Author: Mohamed
# Description: Search for links

from queue import Queue 
from .const import header
from requests import Session 
from bs4 import BeautifulSoup as bs 


class Search(object):

    def __init__(self, dork, proxy):
        self.br = None
        self.proxy = proxy
        self.is_alive = True
        self.links = Queue()
        self.is_testing_proxy = True
        self.is_proxy_working = self.is_working()
        self.url = 'http://www.search-results.com/web?q={0}&page='.format(dork)
    
    def get_br(self):
        session = Session()
        session.headers.update(header)
        session.proxies.update(self.proxy.addr)
        return session

    def is_working(self):
        is_working = True  
        self.br = self.get_br()
        url = 'http://www.search-results.com'

        try:
            self.br.get(url)
        except:
            self.is_proxy_working = False  
            is_working = False 
        
        self.is_testing_proxy = False 

        return is_working
    
    def find_links(self):        
        page = 0
        while self.is_alive:
            page += 1
            url = self.url + str(page)

            html = None 

            try: 
                html = self.br.get(url).content
            except:
                continue 
            
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