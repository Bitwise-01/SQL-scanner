# 12/29/2018
# Author: Mohamed 
# Description: Display 

from os import system
from time import sleep 
from colorama import Fore 
from random import choice 
from platform import system as platform 
from .const import debug, version, banners


class Display(object):

    def __init__(self):
        self.delay = 1.3
        self.is_shutdown = False 
        self.colors_disabled = True 
        self.cls = 'cls' if platform() == 'Windows' else 'clear'
        
    def clear(self):
        if not debug or self.colors_disabled:
            system(self.cls)

            if self.colors_disabled:
                self.colors_disabled = False 
        else:
            print('\n\n')           
    
    def is_vulner(self, link):
        print('{0}[{1}OK{0}] {1}{2}{3}'.format(
            Fore.WHITE, Fore.GREEN, link, Fore.RESET
        ))
    
    def is_not_vulner(self, link):
        print('{0}[{1}NO{0}] {2}{3}{4}'.format(
            Fore.WHITE, Fore.RED, Fore.WHITE, link, Fore.RESET
        ))
       
    def shutdown(self, total=0):
        if total:
            # print('\n{0}[{1}*{0}] {2}Total found: {3}{4}'.format(
            #     Fore.YELLOW, Fore.GREEN, Fore.WHITE, total, Fore.RESET
            # ))

            self.primary('Total found: ' + str(total) )
        else:
            print('')

        print('{0}[{1}!{0}] {2}Shutting Down ...{3}'.format(
            Fore.YELLOW, Fore.RED, Fore.WHITE, Fore.RESET
        ))

        sleep(self.delay)
    
    def info(self, msg):
        print('{0}[{1}i{0}] {2}{3}{4}'.format(
            Fore.YELLOW, Fore.CYAN, Fore.WHITE, msg, Fore.RESET
        ))

        sleep(2.5)
    
    def warning(self, msg):
        print('{0}[{1}!{0}] {1}{2}{3}'.format(
            Fore.YELLOW, Fore.RED, msg, Fore.RESET
        ))

        sleep(self.delay)
    
    def primary(self, data): 
        print('\n\n{0}[{1}*{0}] {2}{3}{4}'.format(
            Fore.YELLOW, Fore.GREEN, Fore.WHITE, data, Fore.RESET
        ))
    
    def banner(self):        
        self.clear() 

        banner = choice(banners)
        color = choice([Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.MAGENTA, Fore.BLUE, Fore.CYAN])

        print(color)
        print(banner.format('{0}V.{1}{2}'.format(Fore.WHITE, version, Fore.RESET)))