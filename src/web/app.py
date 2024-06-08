# -*- coding: utf-8 -*-

import categories_service
import account_service
import cart_service
import bot
from flask import Flask, request, render_template, send_file, session, redirect, url_for, Response
import json
from web3 import Web3

coef = 0.2 # коэффициент начисления баллов

# from eth_account import Account
# from marshmallow import Schema, fields, ValidationError

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
# acc = w3.eth.account.create()
# print(f'private key={w3.to_hex(acc.key)}, account={acc.address}')

w3.eth.defaultAccount = w3.eth.accounts[0]
# Get stored abi and contract_address
with open("contract/MyToken.json", 'r') as f:
    datastore = json.load(f)
    abi = datastore["abi"]
    bytecode = datastore["data"]["bytecode"]["object"]

# set pre-funded account as sender
w3.eth.default_account = w3.eth.accounts[0]

token = w3.eth.contract(abi=abi, bytecode=bytecode)

# Submit the transaction that deploys the contract
tx_hash = token.constructor().transact()

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
token = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=abi
)

# print(token.functions.balanceOf(acc.address).call())
# tx_hash = token.functions.transfer(w3.eth.defaultAccount, acc.address, 1).transact()
#
# tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
#
# print(token.functions.balanceOf(w3.eth.defaultAccount).call())
# print(token.functions.balanceOf(acc.address).call())

# token.functions.greet().call()

app = Flask(__name__)

app.secret_key = b'mmdsadadad#!#$1355...!dd!E'
#session.permanent = True


@app.route("/chipi")
def chipi():
    return render_template("index.html")

@app.route('/my_account', methods=['GET', 'POST'])
def my_account():
    if 'user_id' in session:
        return render_template('my-account.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET'])
def login():
    if 'user_id' not in session:
        return render_template('login.html')
    else:
        return redirect(url_for('my_account'))

@app.route('/login_in', methods=['POST'])
def login_in():
    data = request.get_json()
    res = account_service.login(data['email'], data['password'])
    if res:
        session['user_id'] = data['email']
        #return redirect(url_for('my_account'))
        return "Успешно"
    else:
        return Response("Логин и/или пароль не верны", status=400)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    acc = w3.eth.account.create()
    key = w3.to_hex(acc.key)
    account = acc.address
    res = account_service.register(data['email'], data['password'], account, key)
    if res:
        session['user_id'] = data['email']
        #return redirect(url_for('my_account'))
        return "Успешно"
    else:
        return Response("Этот адрес email уже занят!", status=400)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/header', methods=['GET', 'POST'])
def header():
    return render_template('header.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    return render_template('chat.html')

@app.route('/footer', methods=['GET', 'POST'])
def footer():
    return render_template('footer.html')

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    session['coins_to_pay'] = 0
    if 'user_id' in session:
        return render_template('cart.html')
    else:
        return redirect(url_for('login'))

@app.errorhandler(404)

def not_found(e):
    return render_template("404.html")

@app.route('/category/<code>', methods=['GET', 'POST'])
def open_category(code):
    category = categories_service.get_category(code)
    if category is None:
        return render_template("404.html")
    else:
        return render_template('shop-right-sidebar-list.html',
            category_id=category[0],
            category_name=category[1],
            category_code=category[2]
        )

@app.route('/getCartList', methods=['GET'])
def get_cart_list():
    user_id = session['user_id']
    list = cart_service.get_cart_list(user_id)
    return list

@app.route('/getCategoryList/<code>', methods=['GET'])
def get_category_list(code):
    orderType = request.args.get('orderType')
    list = categories_service.get_category_list(code, orderType)
    return list

@app.route('/category/getImage/<id>', methods=['GET'])
def get_image(id):
    return send_file(f"static/img/{id}", mimetype='image/png')

@app.route('/addToCart/<id>', methods=['POST'])
def add_to_cart(id):
    if 'user_id' not in session:
        return Response("Для выполнения этого действия необходимо быть авторизованным!", status=400)
    else:
        product_id = id
        user_id = session['user_id']
        categories_service.add_to_cart(product_id, user_id)
        return Response("Товар добавлен в корзину!", status=200)

@app.route('/delFromCart/<id>', methods=['POST'])
def del_from_cart(id):
    if 'user_id' not in session:
        return Response("Для выполнения этого действия необходимо быть авторизованным!", status=400)
    else:
        product_id = id
        user_id = session['user_id']
        cart_service.del_from_cart(product_id, user_id)
        return Response("Товар удален из корзины!", status=200)

@app.route('/setAmountInCart/<id>', methods=['POST'])
def set_amount_in_cart(id):
    amount = request.args.get('amount')
    if 'user_id' not in session:
        return Response("Для выполнения этого действия необходимо быть авторизованным!", status=400)
    elif (int(amount) <= 0):
        return Response("Количество должно быть больше 0!", status=500)
    else:
        product_id = id
        user_id = session['user_id']
        cart_service.set_amount_in_cart(product_id, user_id, amount)
        return Response("Товар добавлен в корзину!", status=200)

@app.route('/getTotal', methods=['GET'])
def get_total():
    user_id = session['user_id']
    cart_total = cart_service.get_cart_total(user_id)
    cart_total_str = '{0:,}'.format(cart_total)
    cart_total_str = cart_total_str.replace(",", " ")
    bonus = session["coins_to_pay"]
    if (bonus > cart_total):
        bonus = cart_total
        session["coins_to_pay"] = bonus
    bonus_str = '{0:,}'.format(bonus)
    bonus_str = bonus_str.replace(",", " ")
    total_str = '{0:,}'.format(cart_total - bonus)
    session["total"] = cart_total - bonus
    total_str = total_str.replace(",", " ")
    response = {"cart_total": f"{cart_total_str} ₽", "bonus": f"{bonus_str} ₽", "total": f"{total_str} ₽"}
    return response

@app.route('/getCoinBalance', methods=['GET'])
def get_coin_balance():
    user_id = session['user_id']
    account = cart_service.get_account(user_id)
    balance = token.functions.balanceOf(account).call()
    response = str(balance)
    return response

@app.route('/spendCoins/<amount>', methods=['POST'])
def spend_coins(amount):
    if 'user_id' not in session:
        return Response("Для выполнения этого действия необходимо быть авторизованным!", status=400)
    elif not (amount.isdigit()):
        return Response("Введите целое число!", status=500)
    elif (int(amount) <= 0):
        return Response("Количество должно быть больше 0!", status=500)
    else:
        balance = int(get_coin_balance())
        if (balance < int(amount)):
            return Response("Вы ввели больше баллов, чем у вас есть на счету!", status=500)
        else:
            session['coins_to_pay'] = int(amount)
            return Response("Баллы применены!", status=200)

@app.route('/confirm_order', methods=['POST'])
def confirm_oder():
    if 'user_id' not in session:
        return Response("Для выполнения этого действия необходимо быть авторизованным!", status=400)
    elif (cart_service.get_cart_amount(session['user_id']) <= 0):
        return Response("Корзина пуста!", status=500)
    else:
        user_id = session['user_id']
        account = cart_service.get_account(user_id)
        if (session["coins_to_pay"] == 0):
            bonus = int(coef * session["total"])
            tx_hash = token.functions.transfer(w3.eth.defaultAccount, account, bonus).transact()
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        else:
            tx_hash = token.functions.transfer(account, w3.eth.defaultAccount, session["coins_to_pay"]).transact()
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        cart_service.drop_cart(user_id)
        return Response("Заказ оформлен!", status=200)

@app.route('/ask/<msg>', methods=['POST'])
def ask(msg):

    return Response(bot.response(msg), status=200)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')