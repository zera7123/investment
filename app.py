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
    # cur = mysql.connection.cursor()
    # result = cur.excute("SELECT * FROM mytable WHERE status = 0")
    # if result > 0:
    #     data = cur.fetchall()
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO mytable(name, age) VALUES (%s, %s)", (name, age))
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