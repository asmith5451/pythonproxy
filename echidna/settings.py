"""
Copyright (c) 2016 Kickback Rewards Systems

Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
and associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial 
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import sqlite3
from contextlib import contextmanager

class Settings:
    def __init__(self):
        self.db_path = 'adam2.sqlite'
        
    def servers(self):
        with db_cursor(self.db_path) as cursor:
            cursor.execute("SELECT servers.host, servers.src_port, owners.host, servers.dst_port "
                           "FROM servers JOIN owners ON servers.owner = owners.id LIMIT 1")
            
            for record in cursor:
                yield record
    
    def owners(self):
        with db_cursor(self.db_path) as cursor:
            cursor.execute("SELECT owners.name, owners.host FROM owners")
        
            for record in cursor:
                yield record
    
    def get_dest(self, port):
        with db_cursor(self.db_path) as cursor:
            cursor.execute("SELECT owners.host, servers.dst_port AS port "
                           "FROM servers JOIN owners ON servers.owner = owner.id LIMIT 1")
            
            for record in cursor:
                return record

        return
    
    def add_server(self, name, host, port, owner, dst_port):
        return
    
    def remove_server_by_name(self, name):
        return
    
    def add_owner(self, name, host):
        return
    
    def remove_owner_by_name(self, name):
        return

@contextmanager
def db_cursor(file):
    connection = sqlite3.connect(file)
    yield connection.cursor()
    connection.close()
