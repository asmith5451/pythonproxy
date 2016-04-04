import sqlite3


class SqlReader:
    def __init__(self, src_ip=None, src_port=None, new_owner=None):
        self.src_ip = src_ip
        self.src_port = src_port
        self.new_owner = new_owner

        self.conn = sqlite3.connect('adam2.sqlite')
        self.c = self.conn.cursor()

    def return_record(self):
        record = self.c.execute("SELECT servers.srcip, servers.srcport, owners.destip, servers.destport "
                                "FROM servers JOIN owners ON servers.ownersid = owners.id LIMIT 1")
        return record


class SqlWriter(SqlReader):
    def change_owner(self):
        #TODO: Allow to change owners in sqlite file.
        print('derp')
