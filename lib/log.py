# Date: 01/02/2019
# Author: Mohamed
# Description: Log out vulnerable links

from os import remove
from .const import sql_log
from os.path import exists 


class Log(object):

    def __init__(self, write_over):
        self.mode = 'at'
        self.write_over = write_over
    
    def setup(self):
        if exists(sql_log):            
            if self.write_over:
                remove(sql_log)   
            else:
                self.write(' ')  
            
    def is_in_log(self, link):
        is_in_file = False 

        if not exists(sql_log):
            return False 

        with open(sql_log, 'rt') as f:
            for line in f:
                if line.replace('\n', '') == link:
                    is_in_file = True
        
        return is_in_file        
    
    def write(self, link):

        if not self.is_in_log(link):
            with open(sql_log, self.mode) as f:
                f.write('{}\n'.format(link))