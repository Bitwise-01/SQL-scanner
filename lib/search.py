

import threading
from queue import Queue
from requests_html import HTMLSession


class Search:

    base_url = 'https://bing.com'
    parameters = '/search?q={}'

    def __init__(self, query):
        self.query = query

        self.is_alive = True
        self.is_searching = True

        self.links = Queue()

        self.lock = threading.RLock()

    def next_page(self, html):
        try:
            a = html.find('.b_pag', first=True).find('.b_widePag')
            return self.base_url + a[-1].attrs['href']
        except:
            pass

    def is_valid(self, link):

        if not '=' in link:
            return False

        return True

    def find_links(self):

        session = HTMLSession()
        session.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'

        url = self.base_url + self.parameters.format(self.query)

        while self.is_alive:
            try:
                html = session.get(url).html
            except:
                break

            for r in html.find('.b_algo'):
                a = r.find('h2', first=True).find('a', first=True)

                try:
                    link = a.attrs['href']
                except:
                    continue

                if self.is_valid(link):
                    self.links.put(link)

            next_page = self.next_page(html)

            if not next_page:
                break

            url = next_page

        with self.lock:
            self.is_searching = False

    def get_link(self):
        if self.links.qsize():
            return self.links.get()

    def start(self):

        self.find_links()

    def is_active(self):

        with self.lock:
            is_searching = self.is_searching

        if is_searching or self.links.qsize() > 0:
            return True

        return False

    def stop(self):
        self.is_alive = False
