import requests
from bs4 import BeautifulSoup
import pandas_datareader as pdr
from datetime import datetime, timedelta
from datetime import date
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import re
from decimal import Decimal
import time
import threading

app = Flask(__name__)

# MySQLの設定
app.config['MYSQL_HOST'] = 'zera7123.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'zera7123'
app.config['MYSQL_PASSWORD'] = 'fcc9hEcUNB!5gRK'
app.config['MYSQL_DB'] = 'zera7123$default'

mysql = MySQL(app)

#自動データ取得
def data_thread():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM mytable")
    data = cur.fetchall()
    for row in data:
        if row[14] == 1:
            for i, x in enumerate(row):
                if i == 11:
                    current_id = row[0]
                    current_p = get_stock_price(row[1])
                    cur = mysql.connection.cursor()
                    cur.execute("UPDATE mytable SET current_price = %s WHERE id = %s", (current_p,current_id))
                    mysql.connection.commit()
                    cur.close()
                if i == 13:
                    t_id = row[0]
                    t_price = row[11]
                    cur = mysql.connection.cursor()
                    cur.execute("UPDATE mytable SET t_price = %s WHERE id = %s", (t_price,t_id))
                    mysql.connection.commit()
                    cur.close()
                            
    print("update")
        # データを処理するコードを記述します。
def get_stock_price(stock_code):
    url = f'https://www.google.com/finance/quote/{stock_code}:TYO?hl=ja'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    element = soup.find('div', class_="YMlKec fxKbKc")
    if element is not None:
        element_text = element.get_text()
        stock_price = element_text.replace('￥','').replace(',','')
    else:
        stock_price = 'None'
    return stock_price


if __name__ == '__main__':
    t = threading.Thread(target=data_thread)
    t.start()
    app.run(debug=True)