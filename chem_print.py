#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 14:47:46 2019

@author: shourya
"""

import sqlite3
import csv

f = open("chem.csv","w")
out = csv.writer(f, delimiter=',',quoting=csv.QUOTE_ALL)

conn = sqlite3.connect('chem_db2')
cursor = conn.execute("SELECT * from chem")
for row in cursor:
    name = row[0]
    formula = row[1]
    #n2 = name.strip().lower()
    l = [name,formula]
    out.writerow(l)
    #print(name," - ",formula," - ",n2)
conn.close()
f.close()