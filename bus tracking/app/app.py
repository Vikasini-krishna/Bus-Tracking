from config import SECRET_KEY
from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)
app.config.from_pyfile('config.py')

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'PHW#84#jeor'
app.config['MYSQL_DB'] = 'main'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # To return query results as dictionaries

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        email = request.form['email']
        # address = request.form['address']
        # age = request.form['age']
        # phone = request.form['phone']

        # Hash the password
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        # Store username, hashed password, email, address, age, and phone in the database
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users (username, password, email) VALUES (%s, %s, %s)', (username, hashed_password, email))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('login'))
    return render_template('register.html')
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        # Retrieve the hashed password from the database for the given username
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT password FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Check if the hashed password matches the input password
            if bcrypt.checkpw(password, user['password'].encode('utf-8')):
                # If passwords match, set the user as logged in
                session['logged_in'] = True
                session['email'] = email
                return redirect(url_for('mapping'))
        
        # If login fails, show an error message
        error = 'Invalid email or password. Please try again.'
        return render_template('login.html', error=error)
    
    return render_template('login.html')

@app.route('/mapping', methods=['GET', 'POST'])
def mapping():
  # Check if the user is logged in
  if session.get('logged_in'):
    # Check if the form is submitted and the "enable_location" button is clicked
    if request.method == 'POST' and 'enable_location' in request.form:
      # Redirect to location.html
      return render_template('demo.html')
    # Render the mapping.html page
    return render_template('mapping.html')
  else:
    # If not logged in, redirect to login page
    return redirect(url_for('login'))
@app.route('/location')
def location():
    # Render the location.html page
    return render_template('location.html')
@app.route('/combine', methods=['GET', 'POST'])
def combine():
    # Add any necessary processing here
    return render_template('combine.html')
@app.route('/bus_routes')
def bus_routes():
    return render_template('bus_routes.html')
if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'xyz1234nbg789ty8inmcv2134'
    app.run(debug=True)