from flask import Flask, render_template,  request
from flask_mysqldb import MySQL


app = Flask(__name__)

# Config MySQL
mysql = MySQL()
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hotpink'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        first_name = userDetails['first name']
        last_name = userDetails['last name']
        email = userDetails['email']
        phone = userDetails['phone']
        password = userDetails['password1']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(first_name, last_name, email, phone, password) VALUES(%s, %s, %s, %s, %s)",(first_name, last_name, email, phone, password))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug = True)
