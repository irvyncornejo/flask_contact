from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2012350818CFFDA'
app.config['MYSQL_DB'] = 'contacts'
app.config['MYSQL_PORT'] = 3307
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_contact', methods=['POST'])
def addContact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts_table (full_name, phone, email) '
                    'VALUES (%s, %s, %s )', (fullname, phone, email))

        mysql.connection.commit()

        print('{} | {} | {}'.format(fullname, phone, email))
        return 'Datos recibidos'
@app.route('/edit')
def editContact():
    return 'Edit contact'

@app.route('/delete')
def deleteContact():
    return 'Delete contact'



if __name__ == "__main__":
    app.run(port= 5000, debug= True)