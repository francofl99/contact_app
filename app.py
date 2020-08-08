from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector as db

app = Flask(__name__)

mysql = db.connect(
    host="localhost",
    user="franco",
    password="franco",
    database="Contacts"
)

app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM contacts")
    data = cursor.fetchall()

    return render_template('index.html', contacts=data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        cur = mysql.cursor()

        sql = "INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)"
        val = (fullname, phone, email)

        cur.execute(sql, val)

        mysql.commit()

        flash('Contact Added')

        return redirect(url_for('index'))

@app.route('/edit/<string:id>')
def get_contact(id):
    cursor = mysql.cursor()
    sql = "SELECT * FROM contacts WHERE id = {0}".format(id)
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('edit-contact.html', contact=data[0])


@app.route('/update/<string:id>', methods=['POST'])
def update_contact(id):

    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cursor = mysql.cursor()
        sql = """ 
            UPDATE contacts
            SET fullname = %s,
                phone = %s,
                email = %s
            WHERE id = {0}
        """.format(id)
        val = (fullname, phone, email)
        cursor.execute(sql, val)
        mysql.commit()
        flash("Contact updated successfully")
        return redirect(url_for('index'))


@app.route('/delete/<string:id>')
def delete_contact(id):
    cursor = mysql.cursor()
    sql = "DELETE FROM contacts WHERE id = {0}".format(id) 
    cursor.execute(sql)
    mysql.commit()
    flash("Contact removed successfully")
    return redirect(url_for('index'))

if __name__ == '__main__':
    
    app.run(port=3000, debug=True)

