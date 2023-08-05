import requests
from bs4 import BeautifulSoup
import pandas_datareader as pdr
from datetime import datetime
from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQLの設定
app.config['MYSQL_HOST'] = 'zera7123.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'zera7123'
app.config['MYSQL_PASSWORD'] = 'fcc9hEcUNB!5gRK'
app.config['MYSQL_DB'] = 'zera7123$default'

mysql = MySQL(app)

@app.route('/')
def index():
    # cur = mysql.connection.cursor()
    # result = cur.execute("SELECT * FROM mytable")
    # if result > 0:
    #     data = cur.fetchall()
    # return render_template('index.html', data=data)
    return render_template('total.html')
@app.route('/new')
def new():
    return render_template('new.html')

# @app.route('/total')
# def total():
#     return render_template('total.html')

@app.route('/result', methods=['POST'])
def result():
    stock_code = request.form['stock_code']
    stock_name = get_stock_name(stock_code)
    # start_date = datetime(2022, 1, 1)
    # end_date = datetime(2023, 1, 1)
    # df = pdr.get_data_yahoo(stock_code, start=start_date, end=end_date)
    #return render_template('result.html', stock_name=stock_name, data=df.to_html())
    return render_template('result.html', stock_name=stock_name)

def get_stock_name(stock_code):
    url = f'https://kabutan.jp/stock/?code={stock_code}'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    stock_name = soup.find('h3').text
    return stock_name

if __name__ == '__main__':
    
    
    app.run(debug=True)