from flask import Flask, flash, redirect, render_template, request, url_for, session
from flask_bcrypt import Bcrypt        
app = Flask(__name__)        
bcrypt = Bcrypt(app)
from mysqlconnection import connectToMySQL
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[aA-zZ\s]+$')


@app.route('/')
def index():
    mysql = connectToMySQL("login")
    all_data = mysql.query_db("SELECT * FROM users")
    print (all_data)
    print("Fetched all data", all_data)
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def result():
    email = request.form['email']
    mysql = connectToMySQL("login")
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = {
                'email': request.form['email'],
            
            }
    obj = mysql.query_db(query, data)
    
    print(obj)
    email = request.form['email']
    fname = request.form['fname']
    lname = request.form['lname']
    password = request.form['password']
    cpassword = request.form['cpassword']
    
    if len(request.form['email']) < 1:
        flash("E-mail cannot be blank!")
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!", 'email')
    elif obj:
        flash("Email already exists!", 'email')
        print
    else:
        print("Success you have entered an e-mail")
    
    if len(request.form['fname']) < 1:
        flash('First Name cannot be blank!')
    if len(request.form['fname']) <= 2:
        flash('First Name cannot be less than 2 characters!')
        
        
    elif not NAME_REGEX.match(request.form['fname']):
        flash("Name cannot contain numbers!")
    else:
        print('Success you have entered a first name!')
        
    if len(request.form['lname']) < 1:
        print('Last Name cannot be blank!')
    if len(request.form['fname']) <= 2:
        flash('Last Name cannot be less than 2 characters!')
    elif not NAME_REGEX.match(request.form['lname']):
        flash("Name cannot contain numbers!")
    else:
        print('Success you have entered a last name!')

    if len(request.form['password']) < 8:
        flash('Password must be at least 8 characters')
    elif request.form['password'] != request.form['cpassword']:
        flash('Your Passwords do not match!')
    else:
        print('Success you have entered a password!')
        hpassword = bcrypt.generate_password_hash(password)
        print (hpassword)
    
    if '_flashes' in session.keys():
        print (session['_flashes'])
        return redirect ('/')
    query = "INSERT INTO `login`.`users` (`email`, `first_name`, `last_name`, `password`) VALUES (%(email)s, %(first_name)s, %(last_name)s, %(password)s);"

    data = {
                    'email': request.form['email'],
                    'first_name' : request.form['fname'],
                    'last_name' : request.form['lname'],
                    'password' : hpassword
    }
    mysql = connectToMySQL("login")
    new_email_id = mysql.query_db(query, data)
    return render_template('index.html', email=email, fname=fname, lname=lname, password=password)

@app.route('/login', methods=['POST'])
def login():
    mysql = connectToMySQL("login")
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = {
                'email': request.form['email_check'],
            
            }
    result = mysql.query_db(query, data)
    if  result:
        if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
            session['userid'] = result[0]['id']
            return redirect('/success')
    flash("You could not be logged in")
    return redirect("/")

@app.route('/success')
def success():
    return render_template('success.html')

if __name__=="__main__":
    
    app.run(debug=True) 