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


class SqlReader:
    def __init__(self, src_ip=None, src_port=None, new_owner=None):
        self.src_ip = src_ip
        self.src_port = src_port
        self.new_owner = new_owner

        self.conn = sqlite3.connect('adam2.sqlite')
        self.c = self.conn.cursor()

    def return_record(self):
        record = self.c.execute("SELECT servers.host, servers.src_port, owners.host, servers.dst_port "
                                "FROM servers JOIN owners ON servers.owner = owners.id LIMIT 1")
        return record


class SqlWriter(SqlReader):
    def change_owner(self):
        #TODO: Allow to change owners in sqlite file.
        print('derp')
