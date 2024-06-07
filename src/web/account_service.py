# -*- coding: utf-8 -*-

import random
import json
import sqlite3
from flask import Response



def login(email, password):
    connection = sqlite3.connect('data/shop_db.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM customers WHERE email = '{email}' AND password = '{password}' ")
    res = cursor.fetchone()
    connection.close()
    return res is not None

def register(email, password, account, key):
    connection = sqlite3.connect('data/shop_db.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM customers WHERE email = '{email}' ")
    res = cursor.fetchone()
    if res is None:
        cursor.execute(f"INSERT INTO customers (id, email, password, account, key) VALUES ((SELECT MAX(id) FROM customers) + 1, '{email}', '{password}', '{account}', '{key}')")
        connection.commit()
        connection.close()
        return True
    else:
        return False
