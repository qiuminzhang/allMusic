#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 3/12/2018 4:00 AM
# @Author  : Qiumin Zhang
# @Site    : 
# @File    : mongoDBTest.py
# @Software: PyCharm

from pymongo import MongoClient

# Connect on the default host and server
client = MongoClient('localhost', 27017)
db = client.test_database
collection = db.test_1
inserted_id = collection.insert_one({"firstname": "ZQMMZQ"}).inserted_id
print(inserted_id)
