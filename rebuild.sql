PRAGMA foreign_keys=OFF;
CREATE TABLE owners (id INTEGER PRIMARY KEY, name TEXT, host TEXT);
INSERT INTO "owners" VALUES(1,'ELS-1','localhost');
CREATE TABLE servers (id INTEGER PRIMARY KEY, owner INTEGER, name TEXT, host TEXT, src_port INTEGER UNIQUE, dst_port INTEGER);
INSERT INTO "servers" VALUES(1,1,'POS-1','0.0.0.0',8080,8081);
