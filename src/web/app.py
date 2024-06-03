# -*- coding: utf-8 -*-

import categories_service
import account_service
import cart_service
from flask import Flask, request, render_template, send_file, session, redirect, url_for, Response

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
    res = account_service.register(data['email'], data['password'])
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

@app.route('/footer', methods=['GET', 'POST'])
def footer():
    return render_template('footer.html')

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    session['coins_to_pay'] = 1
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
    bonus_str = '{0:,}'.format(bonus)
    bonus_str = bonus_str.replace(",", " ")
    total_str = '{0:,}'.format(cart_total - bonus)
    total_str = total_str.replace(",", " ")
    response = {"cart_total": f"{cart_total_str} ₽", "bonus": f"{bonus_str} ₽", "total": f"{total_str} ₽"}
    return response

@app.route('/confirm_order', methods=['POST'])
def confirm_oder():
    if 'user_id' not in session:
        return Response("Для выполнения этого действия необходимо быть авторизованным!", status=400)
    elif (cart_service.get_cart_amount(session['user_id']) <= 0):
        return Response("Корзина пуста!", status=500)
    else:
        user_id = session['user_id']
        cart_service.drop_cart(user_id)
        return Response("Заказ оформлен!", status=200)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')