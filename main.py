from flask import Flask, render_template, request, redirect, url_for
import cv2
from random import randint

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib

app = Flask(__name__)

# Change this to your secret key (it can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'mapify'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/mapify/', methods=['GET', 'POST'])
def login():
    # Output a message if something goes wrong...
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


# http://localhost:5000/python/logout - this will be the logout page
@app.route('/mapify/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))



# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/mapify/register', methods=['GET', 'POST'])
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
            # Hash the password
            hash = password + app.secret_key
            hash = hashlib.sha1(hash.encode())
            password = hash.hexdigest()
            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for logged in users
@app.route('/mapify/home')
def home():
    # Check if the user is logged in
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for logged in users
@app.route('/mapify/profile')
def profile():
    # Check if the user is logged in
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not logged in redirect to login page
    return redirect(url_for('login'))


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/service')
def service():
    return render_template('service.html')
@app.route('/team')
def team():
    return render_template('team.html')
@app.route('/why')
def why():
    return render_template('why.html')


@app.route('/upload', methods=['POST'])
def upload():
    image_file = request.files['image']
    # image_location = "F:/Projects/cartotech/final/static/images/" + str(randint(10000, 99999)) + ".jpg"
    image_location = "F:/Projects/cartotech/final/static/images/new.jpg"
    image_file.save(image_location)

    # Perform canopy detection using OpenCV (replace with your specific logic)
    image = cv2.imread(image_location)
    original_image = cv2.imwrite("F:/Projects/cartotech/final/static/output/original.jpg", image)

    # ... (Canopy detection code using OpenCV)
    # Redirect to the result page with a success message and the image location
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gray_image = cv2.imwrite("F:/Projects/cartotech/final/static/output/gray.jpg", gray)


    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV +cv2.THRESH_OTSU)
    # ret, thresh = cv2.threshold(gray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    img_copy = image.copy()

    img_copy = cv2.drawContours(img_copy, contours, -1, (0, 255, 0), 2)
    contour_image = cv2.imwrite("F:/Projects/cartotech/final/static/output/contour.jpg", img_copy)


    canimg = cv2.Canny(gray, 50, 200)
    bcontour_image = cv2.imwrite("F:/Projects/cartotech/final/static/output/bcontour.jpg", thresh)
    canny_image = cv2.imwrite("F:/Projects/cartotech/final/static/output/canny.jpg", canimg)

    # Create default parametrization LSD
    lsd = cv2.createLineSegmentDetector(0)
    # Apply to the edge detection image
    lines = lsd.detect(gray)[0]
    # Draw detected lines in the image on new white background
    drawn_img = lsd.drawSegments(image, lines)
    lsd_image = cv2.imwrite("F:/Projects/cartotech/final/static/output/lsd.jpg", drawn_img)

    import numpy as np
    # Hough line
    lines = cv2.HoughLinesP(thresh,1,np.pi/180,10)
    for line in lines:
        x1,y1,x2,y2 = line[0]
        cv2.line(image,(x1,y1),(x2,y2),(0,255,255),2)
    hough_image = cv2.imwrite("F:/Projects/cartotech/final/static/output/hough.jpg", image)


    return redirect(url_for('display_output', filename="original.jpg" ))

@app.route('/output/<filename>')
def display_output(filename):
    return render_template('service.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
