from flask import Flask, request, render_template
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
    cur = mysql.connection.cursor()
    result = cur.excute("SELECT * FROM mytable")
    if result > 0:
        data = cur.fetchall()
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        b_price = request.form['b_price']
        b_date = request.form['b_date']
        b_reason = request.form['b_reason']
        s_price = request.form['s_price']
        s_date = request.form['s_date']
        s_reason = request.form['s_reason']
        status = request.form['status']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO mytable(code, name, b_price, b_date, b_reason, s_price, s_date, s_reason, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (code, name, b_price, b_date, b_reason, s_price, s_date, s_reason, status))
        mysql.connection.commit()
        cur.close()
        return 'success'

@app.route('/data')
def data():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM mytable")
    if result > 0:
        data = cur.fetchall()
        return render_template('data.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)