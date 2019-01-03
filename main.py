# Date: 01/02/2019
# Author: Mohamed
# Description: SQL Vulnerability Scanner

from lib.sql import SQL 
from lib.display import Display
from argparse import ArgumentParser


class Engine(object):

    def __init__(self, dork, write_over): 
        self.dork = dork 
        self.display = Display() 
        self.sql = SQL(dork, write_over) 

    def start(self):        
        self.display.banner()
        self.display.primary('Dork: ' + self.dork)

        try: 
            self.sql.start() 
        except KeyboardInterrupt:
            pass 
        finally:
            self.stop()
    
    def stop(self):
            
        if self.sql:
            self.sql.stop()
        else:
            self.display.shutdown()

def args():
    args = ArgumentParser()
    args.add_argument('-d', '--dork', required=True, help='dork to search example: product.php?id=')
    args.add_argument('-w', '--write-over', dest='writeover', default=False, action='store_true', help='write over the existing log file')
    return args.parse_args()    


if __name__ == '__main__':
    arugments = args()    
    Engine(arugments.dork, arugments.writeover).start()  