import requests
from bs4 import BeautifulSoup
import pandas_datareader as pdr
from datetime import datetime
from datetime import date
from flask import Flask, render_template, request
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
    for row in data:
        formatted_row = []
        for i, x in enumerate(row):
            if i == 1:
               stock_price = get_stock_price(row[1]) 
               formatted_row.append(str(x))
            elif i == 3:
                stock_b_price = row[3]
                formatted_row.append(str(x))
            elif i == 4:
                stock_number = row[4]
                formatted_row.append(str(x))
            elif i == len(row) - 1:
                formatted_row.append(str(x))
                formatted_row.append(stock_price)
                stock_price_number = Decimal(stock_price) * stock_number
                stock_b_price_number = stock_b_price * stock_number
                p_and_l = stock_price_number - stock_b_price_number
                formatted_row.append(stock_price_number)
                formatted_row.append(p_and_l)
            else:
                # その他の列はそのまま表示
                formatted_row.append(str(x))
        formatted_data.append(formatted_row)
        print(formatted_data)
        
    return render_template('index.html', data=formatted_data)

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
        result = cur.execute("SELECT * FROM mytable")
        if result > 0:
                data = cur.fetchall()
        cur.close()
        return render_template('index.html', data=data)

# @app.route('/total')
# def total():
#     return render_template('total.html')

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
    stock_name = element.get_text()
    return stock_name

def get_stock_price(stock_code):
    url = f'https://www.google.com/finance/quote/{stock_code}:TYO?hl=ja'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    element = soup.find('div', class_="YMlKec fxKbKc")
    element_text = element.get_text()
    stock_price = element_text.replace('￥','').replace(',','')
    return stock_price

if __name__ == '__main__':
    
    
    app.run(debug=True)