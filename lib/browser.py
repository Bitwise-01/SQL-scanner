# Date: 12/28/2018
# Author: Mohamed
# Description: Browser

import requests
from time import time
from requests import Session


class Browser(object):

    def __init__(self, link):
        self.link = link
        self.is_active = True
        self.start_time = None
        self.is_vulner = False
        self.is_attempted = False

    def get_content(self):
        try:
            return requests.get(self.link + '*').text.lower()
        except:
            pass

    def attempt(self):
        self.start_time = time()
        content = self.get_content()

        if content:
            self.is_attempted = True

            if 'sql' in content and 'error' in content and 'at line' in content:
                self.is_vulner = True

        self.is_active = False
