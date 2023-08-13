import requests
from bs4 import BeautifulSoup
import pandas_datareader as pdr
from datetime import datetime
from datetime import date
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import re
from decimal import Decimal

app = Flask(__name__)

# MySQLの設定
app.config['MYSQL_HOST'] = 'zera7123.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'zera7123'
app.config['MYSQL_PASSWORD'] = 'fcc9hEcUNB!5gRK'
app.config['MYSQL_DB'] = 'zera7123$default'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM mytable")
    data = cur.fetchall()
        
     # データを整形
    formatted_data = []
    p_and_l_total = 0
    for row in data:
        if row[12] == 1:
            formatted_row = []
            for i, x in enumerate(row):
                if i == 3:
                    stock_b_price = row[3]
                    if stock_b_price is not None:
                        stock_b_price_for = format(stock_b_price,',') 
                        formatted_row.append(stock_b_price_for)
                    else:
                        formatted_row.append(stock_b_price)
                elif i == 4:
                    stock_number = row[4]
                    formatted_row.append(str(x))
                elif i == 7:
                    stock_s_price = row[7]
                    if stock_s_price is not None:
                        stock_s_price_for = format(stock_s_price,',') 
                        formatted_row.append(stock_s_price_for)
                    else:
                        formatted_row.append(stock_s_price)
                elif i == len(row) - 1:
                    if row[11] is not None:
                        stock_price = Decimal(row[11])
                    else:
                        stock_price = Decimal('0')
                    formatted_row.append(str(x))
                    if stock_price is not None:
                        stock_price_for = format(stock_price,',')
                        formatted_row.append(stock_price_for)
                    else:
                        formatted_row.append(stock_price)
                    stock_price_number = stock_price * stock_number
                    if stock_price_number is not None:
                        stock_price_number_for = format(stock_price_number,',')
                        formatted_row.append(stock_price_number_for)
                    else:
                        formatted_row.append(stock_price_number)
                    stock_b_price_number = stock_b_price * stock_number
                    p_and_l = stock_price_number - stock_b_price_number
                    p_and_l_for = format(p_and_l,',')
                    p_and_l_total += p_and_l
                
                    formatted_row.append(p_and_l_for)
                else:
                    # その他の列はそのまま表示
                    formatted_row.append(str(x))
            formatted_data.append(formatted_row)
    
    p_and_l_total_for = format(p_and_l_total,',')   
        
    return render_template('index.html', data=formatted_data, data2=p_and_l_total_for)

@app.route('/c_price')
def c_price():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM mytable")
    data = cur.fetchall()
    
    for row in data:
        if row[12] == 1:
            for i, x in enumerate(row):
                if i == 11:
                    current_id = row[0]
                    current_p = get_stock_price(row[1])
                    cur = mysql.connection.cursor()
                    cur.execute("UPDATE mytable SET current_price = %s WHERE id = %s", (current_p,current_id))
                    mysql.connection.commit()
                    cur.close()
    
    return redirect(url_for('index'))

@app.route('/new')
def new():
    return render_template('new.html')

@app.route('/sign_up', methods=['POST'])
def sign_up():
    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        b_price = request.form['b_price']
        b_number = request.form['b_number']
        b_date = request.form['b_date']
        b_reason = request.form['b_reason']
        status = 1
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO mytable(code, name, b_price, b_number, b_date, b_reason, status) VALUES (%s, %s, %s, %s, %s, %s, %s)", (code, name, b_price, b_number, b_date, b_reason, status))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

@app.route('/total')
def total():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM mytable")
    data = cur.fetchall()
        
     # データを整形
    formatted_data = []
    p_and_l_total = 0
    for row in data:
        if row[12] == 1:
            formatted_row = []
            for i, x in enumerate(row):
                if i == 3:
                    stock_b_price = row[3]
                    if stock_b_price is not None:
                        stock_b_price_for = format(stock_b_price,',') 
                        formatted_row.append(stock_b_price_for)
                    else:
                        formatted_row.append(stock_b_price)
                elif i == 4:
                    stock_number = row[4]
                    formatted_row.append(str(x))
                elif i == 7:
                    stock_s_price = row[7]
                    if stock_s_price is not None:
                        stock_s_price_for = format(stock_s_price,',') 
                        formatted_row.append(stock_s_price_for)
                    else:
                        formatted_row.append(stock_s_price)
                elif i == len(row) - 1:
                    formatted_row.append(str(x))
                    if stock_s_price is not None:
                        stock_s_price_number = stock_s_price * stock_number
                    else:
                        stock_s_price_number = 0
                    stock_b_price_number = stock_b_price * stock_number
                    p_and_l = stock_s_price_number - stock_b_price_number
                    p_and_l_for = format(p_and_l,',')
                    p_and_l_total += p_and_l
                
                    formatted_row.append(p_and_l_for)
                else:
                    # その他の列はそのまま表示
                    formatted_row.append(str(x))
            formatted_data.append(formatted_row)
    
    p_and_l_total_for = format(p_and_l_total,',')   
       
    

    return render_template('total.html', data=formatted_data, data2=p_and_l_total_for)

@app.route('/data')
def data():
    arg1 = request.args.get('arg1')
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM mytable")
    data = cur.fetchall()   
    
    formatted_data = []
    
    for row in data:
        com0 = int(row[0])
        com1 = int(arg1)
        if com0 == com1:
            formatted_data.append(row[0])
            formatted_data.append(row[1])
            formatted_data.append(row[2])
            stock_b_price = row[3]
            if stock_b_price is not None:
                stock_b_price_for = format(stock_b_price,',')
                formatted_data.append(stock_b_price_for)
            else:
                formatted_data.append(stock_b_price)
            formatted_data.append(row[4])
            formatted_data.append(row[5])
            formatted_data.append(row[6])
            stock_s_price = row[7]
            if stock_s_price is not None:
                stock_s_price_for = format(stock_s_price,',')
                formatted_data.append(stock_s_price_for)
            else:
                formatted_data.append(stock_s_price)
            formatted_data.append(row[8])
            formatted_data.append(row[9])
            formatted_data.append(row[10])               
            stock_c_price = row[11]
            if stock_c_price is not None:
                stock_c_price_for = format(stock_c_price,',')
                formatted_data.append(stock_c_price_for)
            else:
                formatted_data.append(stock_c_price)                  
            stock_number = row[4]
            if stock_b_price is not None:
                stock_b_price_number = stock_b_price * stock_number
            else:
                stock_b_price_number = 0
            if stock_c_price is not None:
                stock_c_price_number = stock_c_price * stock_number
            else:
                stock_c_price_number = 0   
            if stock_c_price_number is not None:
                stock_c_price_number_for = format(stock_c_price_number,',')
                formatted_data.append(stock_c_price_number_for)
            else:
                formatted_data.append(stock_c_price_number) 
            p_and_l = stock_c_price_number - stock_b_price_number
            if p_and_l is not None:
                p_and_l_for = format(p_and_l,',')
                formatted_data.append(p_and_l_for)
            else:
                formatted_data.append(p_and_l)
               
    return render_template('data.html',data = formatted_data)

@app.route('/add_buy', methods=['POST'])
def add_buy():
    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        b_price = request.form['b_price']
        b_number = request.form['b_number']
        b_date = request.form['b_date']
        b_reason = request.form['b_reason']
        status = 1
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO mytable(code, name, b_price, b_number, b_date, b_reason, status) VALUES (%s, %s, %s, %s, %s, %s, %s)", (code, name, b_price, b_number, b_date, b_reason, status))
        mysql.connection.commit()
        cur.close()      
    return redirect(url_for('index'))

@app.route('/sell', methods=['POST'])
def sell():
    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        b_price = request.form['b_price']
        b_number = request.form['b_number']
        b_date = request.form['b_date']
        b_reason = request.form['b_reason']
        status = 1
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO mytable(code, name, b_price, b_number, b_date, b_reason, status) VALUES (%s, %s, %s, %s, %s, %s, %s)", (code, name, b_price, b_number, b_date, b_reason, status))
        mysql.connection.commit()
        cur.close()      
    return redirect(url_for('index'))


@app.route('/result', methods=['POST'])
def result():
    stock_code = request.form['stock_code']
    stock_name = get_stock_name(stock_code)
    stock_price = get_stock_price(stock_code)
    today = date.today()
    # start_date = datetime(2022, 1, 1)
    # end_date = datetime(2023, 1, 1)
    # df = pdr.get_data_yahoo(stock_code, start=start_date, end=end_date)
    #return render_template('result.html', stock_name=stock_name, data=df.to_html())
    return render_template('new.html', stock_name=stock_name, stock_code=stock_code, stock_price=stock_price, today=today)

def get_stock_name(stock_code):
    url = f'https://www.google.com/finance/quote/{stock_code}:TYO?hl=ja'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    element = soup.find('div', class_="zzDege")
    if element.get_text() is not None:
        stock_name = element.get_text()
    else:
        stock_name = 'None'
    return stock_name

def get_stock_price(stock_code):
    url = f'https://www.google.com/finance/quote/{stock_code}:TYO?hl=ja'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    element = soup.find('div', class_="YMlKec fxKbKc")
    if element.get_text() is not None:
        element_text = element.get_text()
        stock_price = element_text.replace('￥','').replace(',','')
    else:
        stock_price = 'None'
    return stock_price

if __name__ == '__main__':
    
    
    app.run(debug=True)