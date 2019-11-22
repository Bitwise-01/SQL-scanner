# Date: 01/02/2019
# Author: Mohamed
# Description: SQL checker

from .log import Log
from .search import Search
from .browser import Browser
from time import sleep, time
from .display import Display
from threading import Thread, RLock
from .const import max_time_to_wait, max_active_browsers


class SQL(object):

    def __init__(self, dork, write_over):
        self.links = []
        self.dork = dork
        self.browsers = []
        self.search = None
        self.lock = RLock()
        self.is_alive = True
        self.total_found = 0
        self.active_links = []
        self.display = Display()
        self.log = Log(write_over)

    def search_manager(self):
        search = Search(self.dork)
        self.search = search

        Thread(target=self.search.start, daemon=True).start()

        while self.is_alive:

            if not self.search.is_active():
                break
            else:
                link = self.search.get_link()
                if link:
                    with self.lock:
                        self.links.append(link)
                else:
                    sleep(0.5)

        if self.is_alive:
            self.is_alive = False

    def link_manager(self):
        is_started = False

        while self.is_alive:

            if not self.search:
                sleep(1.5)
                continue

            if not self.search.links.qsize():
                continue

            browsers = []
            for link in self.links:

                if not link in self.active_links and len(self.active_links) < max_active_browsers:
                    self.active_links.append(link)
                    browser = Browser(link)
                    browsers.append(browser)
                    self.browsers.append(browser)

            for browser in browsers:

                if not is_started and self.is_alive:
                    self.display.info('Starting vulnerability scanner ...\n')
                    is_started = True

                if not self.is_alive:
                    break

                t = Thread(target=browser.attempt)
                t.daemon = True
                t.start()

    def browser_manager(self):
        while self.is_alive:

            for browser in self.browsers:

                if not self.is_alive:
                    break

                if not browser.is_active:

                    if browser.is_attempted:
                        with self.lock:
                            if browser.link in self.links:
                                self.links.remove(browser.link)

                        if browser.is_vulner:
                            self.total_found += 1
                            self.log.write(browser.link)
                            self.display.is_vulner(browser.link)
                        else:
                            self.display.is_not_vulner(browser.link)

                    with self.lock:
                        self.active_links.remove(browser.link)
                        self.browsers.remove(browser)

                if browser.start_time:
                    if time() - browser.start_time >= max_time_to_wait:
                        browser.is_active = False

    def start(self):
        try:
            self.log.setup()
        except KeyboardInterrupt:
            self.stop()
        except:
            pass

        if not self.is_alive:
            return

        self.display.info('Starting daemon threads ...')
        link_manager = Thread(target=self.link_manager)
        link_manager.daemon = True
        link_manager.start()

        search_manager = Thread(target=self.search_manager)
        search_manager.daemon = True
        search_manager.start()

        self.browser_manager()

    def stop(self):
        if self.search:
            self.search.stop()

        self.is_alive = False
        self.display.shutdown(self.total_found)
