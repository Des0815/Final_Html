from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于安全地保存会话数据

# 示例商品清单
products = [
    {"id": 1, "name": "一日通行證", "price": 1580},
    {"id": 2, "name": "两日通行證", "price": 2080}
]

@app.route('/')
def index():
    return render_template('mainpage.html', products=products)

@app.route('/mainpage')
def mainpage():
    return render_template('mainpage.html', products=products)

@app.route('/buy', methods=['POST'])
def buy_tickets():
    ticket_id = request.form.get('ticket_id')
    quantity = int(request.form.get('quantity'))
    payment_method = request.form.get('payment_method')

    # 查找选中的票种信息
    ticket_info = next((product for product in products if str(product['id']) == ticket_id), None)
    if ticket_info:
        total_price = ticket_info['price'] * quantity

        # 保存购票信息到会话中，以便在重定向后使用
        session['ticket_info'] = ticket_info
        session['quantity'] = quantity
        session['total_price'] = total_price
        session['payment_method'] = payment_method

        # 跳转到付款选择页面
        return redirect(url_for('choose_payment'))
    else:
        # 处理无效的票种选择
        return "Invalid ticket selection", 400

@app.route('/choose_payment')
def choose_payment():
    return render_template('choose_payment.html')

@app.route('/process_payment', methods=['POST'])
def process_payment():
    payment_method = request.form.get('payment_method')

    # 在这里处理付款逻辑
    # ...

    # 假设付款成功，重定向到付款成功页面
    return redirect(url_for('payment_success'))

@app.route('/payment_success')
def payment_success():
    # 可以从会话中获取付款信息以显示在付款成功页面
    return render_template('payment_success.html')

@app.route('/success')
def success():
    # 从会话获取购票信息
    ticket_info = session.get('ticket_info')
    quantity = session.get('quantity')
    total_price = session.get('total_price')
    payment_method = session.get('payment_method')

    return render_template('success.html', ticket_type=ticket_info['name'], quantity=quantity, total_price=total_price, payment_method=payment_method)


@app.route('/loginregister')
def loginregister():
    return render_template('loginregister.html')

@app.route('/buyticket')
def buyticket():
    return render_template('buyticket.html')


if __name__ == '__main__':
    app.run(debug=True)
    
