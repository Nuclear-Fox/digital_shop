# -*- coding: utf-8 -*-

import random
import json
import sqlite3
from flask import Response



def get_category(code):
    connection = sqlite3.connect('data/shop_db.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM categories_info WHERE code = '{code}'")
    category = cursor.fetchone()
    connection.close()
    return category

def get_category_list(code, orderType):
    connection = sqlite3.connect('data/shop_db.db')
    cursor = connection.cursor()
    query =    f" SELECT pr.id, pr.name, pr.price, pr.info, pr.brand FROM categories" \
               f" INNER JOIN categories_info ON categories.category_id = categories_info.category_id " \
               f" AND categories_info.code = '{code}' " \
               f" INNER JOIN products pr ON categories.product_id = pr.id "
    if orderType == '1':
        query += f" ORDER BY pr.id"
    elif orderType == '2':
        query += f" ORDER BY pr.price"
    elif orderType == '3':
        query += f" ORDER BY pr.price DESC"

    cursor.execute(query)
    list = cursor.fetchall()
    connection.close()
    return list

def add_to_cart(product_id, user_id):
    connection = sqlite3.connect('data/shop_db.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT *  FROM carts WHERE cust_id = (SELECT id FROM customers WHERE email = '{user_id}') AND product_id = {product_id}")

    if cursor.fetchone() is None:
        res = cursor.execute(f"INSERT INTO carts VALUES ((SELECT id FROM customers WHERE email = '{user_id}'), {product_id}, 1)")
    else:
        res = cursor.execute(f"UPDATE carts SET amount = amount + 1 WHERE cust_id = (SELECT id FROM customers WHERE email = '{user_id}') AND product_id = {product_id}")
    connection.commit()
    connection.close()
