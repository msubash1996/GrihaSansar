import tempfile
from flask import Flask, request, jsonify, render_template
from flask import redirect, session, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import util
import tkinter as tk

app = Flask(__name__, template_folder="/home/subash/Desktop/Nepal-Homes-master/client", static_folder="/home/subash/Desktop/Nepal-Homes-master/client")
app.secret_key = 'Subash@32!'

@app.route('/')
def index():
    return render_template('index.html',url_for=url_for)



@app.route('/price_estimate')
def price_estimate():
    return render_template('app.html')


@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    response = jsonify({
        'estimated_price': str(util.get_estimated_price(location,bhk,bath,total_sqft,))
    })

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response



app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'subash'
app.config['MYSQL_PASSWORD'] = 'Od00'
app.config['MYSQL_DB'] = 'grihasansar'
 
mysql = MySQL(app)
 
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
  # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone() 
        
            # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'           
        # Show the login form with message (if any)
    return render_template('login.html', msg=msg)


    # http://localhost:5000/logout - this will be the logout page@app.route('/logout')
@app.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()

        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'

    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)



# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('index.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))    

@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/buy_house',methods=['GET', 'POST'])
def buy_house():
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'phone' in request.form and 'location' in request.form and  'budget' in request.form and 'message' in request.form:
        # Create variables for easy access
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        location = request.form['location']
        budget = request.form['budget']
        message = request.form['message']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # cursor.execute('INSERT INTO buyers VALUES (NULL, %s, %s, %s)', (name, email, phone, location,budget, message))
        cursor.execute('INSERT INTO buyers VALUES (NULL, %s, %s, %s, %s, %s, %s)', (name, email, phone, location, budget, message))

        mysql.connection.commit()
        msg = 'Your form is submitted.!'

    return render_template('buy.html')

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    print(app.template_folder)
    app.run(port=5600)