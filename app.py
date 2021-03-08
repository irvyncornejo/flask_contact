from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'usuario'
app.config['MYSQL_PASSWORD'] = 'contraseña'
app.config['MYSQL_DB'] = 'contacts'
app.config['MYSQL_PORT'] = 3307
mysql = MySQL(app)

#Session
app.secret_key = 'millavesecreta'

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute(' SELECT * FROM contacts_table')
    data = cur.fetchall()
    return render_template('index.html', contacts = data)

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
        flash('Contact added successfully')
        print('{} | {} | {}'.format(fullname, phone, email))
        return redirect(url_for('index'))

@app.route('/edit/<id>')
def get_contact(id): 
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts_table WHERE user_id={}'.format(id))
    data = cur.fetchone()
    print(data)
    return render_template('edit-contact.html', contact = data)

@app.route('/delete/<string:id>')
def deleteContact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM  contacts_table WHERE user_id= {}'.format(id))
    mysql.connection.commit()
    flash('Contact deleted')
    return redirect(url_for('index'))

@app.route('/update/<id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

    cur = mysql.connection.cursor()
    cur.execute('UPDATE contacts_table SET full_name=%s, phone =%s, email=%s WHERE user_id=%s' , (fullname, phone, email, id))
    mysql.connection.commit()
    
    flash('Contact updated')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(port= 5000, debug= True)
