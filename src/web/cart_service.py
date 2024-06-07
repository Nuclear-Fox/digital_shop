# -*- coding: utf-8 -*-

import random
import json
import sqlite3
from flask import Response

def get_cart_list(user_id):
    connection = sqlite3.connect('data/shop_db.db')
    cursor = connection.cursor()
    query =    f" SELECT " \
               f" carts.product_ID AS id, " \
               f" products.name AS name, " \
               f" products.price AS price, " \
               f" carts.amount AS amount, " \
               f" carts.amount * products.price AS total " \
               f" FROM carts " \
               f" INNER JOIN customers ON cust_id = customers.id " \
               f" AND customers.email = '{user_id}' " \
               f" INNER JOIN products ON product_id = products.id; "

    cursor.execute(query)
    list = cursor.fetchall()
    connection.close()
    return list

def set_amount_in_cart(product_id, user_id, amount):
    connection = sqlite3.connect('data/shop_db.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT *  FROM carts WHERE cust_id = (SELECT id FROM customers WHERE email = '{user_id}') AND product_id = {product_id}")

    if cursor.fetchone() is None:
        res = cursor.execute(f"INSERT INTO carts VALUES ((SELECT id FROM customers WHERE email = '{user_id}'), {product_id}, {amount})")
    else:
        res = cursor.execute(f"UPDATE carts SET amount = {amount} WHERE cust_id = (SELECT id FROM customers WHERE email = '{user_id}') AND product_id = {product_id}")
    connection.commit()
    connection.close()

def del_from_cart(product_id, user_id):
    connection = sqlite3.connect('data/shop_db.db')
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM carts WHERE cust_id = (SELECT id FROM customers WHERE email = '{user_id}') AND product_id = {product_id}")
    connection.commit()
    connection.close()

def drop_cart(user_id):
    connection = sqlite3.connect('data/shop_db.db')
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM carts WHERE cust_id = (SELECT id FROM customers WHERE email = '{user_id}')")
    connection.commit()
    connection.close()

def get_cart_total(user_id):
    connection = sqlite3.connect('data/shop_db.db')
    cursor = connection.cursor()
    query =    f" SELECT SUM(total) AS cart_total FROM (" \
               f" SELECT " \
               f" carts.amount * products.price AS total " \
               f" FROM carts " \
               f" INNER JOIN customers ON cust_id = customers.id " \
               f" AND customers.email = '{user_id}' " \
               f" INNER JOIN products ON product_id = products.id " \
               f" ) AS prices "
    cursor.execute(query)
    total = cursor.fetchone()[0]
    connection.close()
    return total

def get_cart_amount(user_id):
    connection = sqlite3.connect('data/shop_db.db')
    cursor = connection.cursor()
    query =    f" SELECT " \
               f" SUM(carts.amount) AS total_amount " \
               f" FROM carts " \
               f" INNER JOIN customers ON cust_id = customers.id " \
               f" AND customers.email = '{user_id}' " \
               f" INNER JOIN products ON product_id = products.id "
    cursor.execute(query)
    amount = cursor.fetchone()[0]
    connection.close()
    if amount is None:
        return 0
    else:
        return amount

def get_account(user_id):
    connection = sqlite3.connect('data/shop_db.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT account FROM customers WHERE email = '{user_id}' ")
    account = cursor.fetchone()[0]
    connection.close()
    if account is None:
        return ""
    else:
        return account
