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
import os
from contextlib import contextmanager

class SettingsError(Exception):
    pass

class Settings:
    def __init__(self, working_directory):
        self.db_path = os.path.join(working_directory, 'adam2.sqlite')
        
    def servers(self):
        yield from self.query(
            "SELECT servers.host, servers.src_port, owners.host, servers.dst_port "
            "FROM servers JOIN owners ON servers.owner = owners.id LIMIT 1")
    
    def owners(self):
        yield from self.query(
            "SELECT owners.name, owners.host FROM owners")
    
    def get_dest(self, port):
        yield from self.query(
            "SELECT owners.host, servers.dst_port AS port "
            "FROM servers JOIN owners ON servers.owner = owner.id LIMIT 1")
    
    def add_server(self, name, host, port, owner, dst_port):
        return
    
    def remove_server_by_name(self, name):
        return
    
    def add_owner(self, name, host):
        return
    
    def remove_owner_by_name(self, name):
        return
    
    def query(self, query):
        with db_cursor(self.db_path) as cursor:
            try:
                cursor.execute(query)
            except sqlite3.DatabaseError as err:
                raise SettingsError(err)
            for record in cursor:
                yield record    

@contextmanager
def db_cursor(file):
    connection = None
    try:
        connection = sqlite3.connect(file)
    except:
        raise SettingsError("failed to open configuration database")
    yield connection.cursor()
    connection.close()
