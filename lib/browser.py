# Date: 12/28/2018
# Author: Mohamed
# Description: Browser

from time import time 
from requests import Session
from .const import header, fetch_time, debug


class Browser(object):

    def __init__(self, link, proxy):
        self.link = link 
        self.proxy = proxy 
        self.is_active = True 
        self.start_time = None 
        self.is_vulner = False 
        self.browser = self.br()
        self.is_attempted = False 
        
    def br(self):
        session = Session()
        session.headers.update(header)
        session.proxies.update(self.proxy.addr)
        return session 

    def get_content(self):
        resp = None 
        url = self.link + '\''

        try:
            resp = self.browser.get(url, timeout=fetch_time).text  
        except:
            pass 
        
        return resp 
               
    def attempt(self):
        self.start_time = time()
        content = self.get_content()
        
        if content:
            self.is_attempted = True 
            
            if 'Invalid SQL' in content or 'error' in content:
                self.is_vulner = True            

        self.is_active = False