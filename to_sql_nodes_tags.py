#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' writes nodes_tags csv to nodes_tags sql table '''

import sqlite3
import csv
from pprint import pprint

sqlite_file = 'osm.db'    # name of the sqlite database file

# Connect to the database
conn = sqlite3.connect(sqlite_file)
# Get a cursor object
cur = conn.cursor()
cur.execute('''DROP TABLE IF EXISTS nodes_tags''')
conn.commit()
# Create the table, specifying the column names and data types:
cur.execute('''
    CREATE TABLE nodes_tags (
    id INTEGER,
    key TEXT,
    value TEXT,
    type TEXT,
    FOREIGN KEY (id) REFERENCES nodes(id)
);
''')
# commit the changes
conn.commit()
# Read in the csv file as a dictionary, format the
# data as a list of tuples:
with open('nodes_tags.csv','rb') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'].decode("utf-8"), i['key'].decode("utf-8"), i['value'].decode("utf-8"), i['type'].decode("utf-8")) for i in dr]
# insert the formatted data
cur.executemany("INSERT INTO nodes_tags(id, key, value,type) VALUES (?, ?, ?, ?);", to_db)
# commit the changes
conn.commit()
cur.execute('SELECT * FROM nodes_tags')
all_rows = cur.fetchall()
print('1):')
pprint(all_rows)
conn.close()
