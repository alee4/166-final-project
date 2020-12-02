
# https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/
# https://pynative.com/python-generate-random-string/

import sqlite3
from flask import Flask, render_template, redirect, url_for, request, flash
from database import *
import sqlite3

blackList = ["--", ";", "/*", "*/", "@@", "@", "%", "\""]

loginAttempts = -23456
# create the application object
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/", methods=['GET', 'POST'])
def login():
    global correctUserName
    global accessLevel
    global loginAttempts

    if loginAttempts == 3:
        return redirect(url_for('maxLogins'))


    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        pw_hash = hash_pw(password)

        # check for sql code in the loging inputs
        sqlInjectionFound = False
        i = 0
        j = 0
        while i < len(blackList):
            if blackList[i] in username:
                errorMessage = "An SQL term has been detected, the website will now crash."
                print(errorMessage)
                sqlInjectionFound = True
            i = i + 1

        while j < len(blackList):
            if blackList[j] in password:
                errorMessage = "An SQL term has been detected, the website will now crash."
                print(errorMessage)
                sqlInjectionFound = True
            j = j + 1

        if sqlInjectionFound:
            loginAttempts = loginAttempts + 1
            print(loginAttempts)
            redirect(url_for('not_login_success'))

        print(username + " " + password)
        #check to make sure that the username is in the database
        conn = sqlite3.connect('userData.db')

        # conn.row_factory = sqlite3.Row
        c = conn.cursor()
        t = (username,)
        c.execute('SELECT * FROM userDatas WHERE userName=?', t)

        data1 = []
        try:
            #gets the data at the row matching the inputted user name
            for row in c.execute('SELECT * FROM userDatas WHERE userName=?', t):
                #sets the data to a array thing
                data1 = row

            # todo- fix this bruh
            #now allows it so i can check to see if database username is euqal to inputted username
            #and same for pass, if both are equal, sends to login page
            # if data1[0] == username and data1[1] == pw_hash:
            if data1[0] == username and authenticate(data1[1], pw_hash, 80):
                print("login success")
                correctUserName = data1[0]
                accessLevel = data1[2]
                return redirect(url_for('login_success'))
            else:  #else, just redirects back to unsuccessful page
                print("data[1]: " + data1[1])
                print("pw_hash: " + pw_hash)
                print("Login unsuccessful")
                loginAttempts = loginAttempts + 1
                print(loginAttempts)
                return redirect(url_for('not_login_success'))
        except IndexError:  #if the initial username is not correct, just redirects to unsuccessful login
            print("dataNotFound")
            loginAttempts = loginAttempts + 1
            print(loginAttempts)
            return redirect(url_for('not_login_success'))

        print(c.fetchone())
        data = c.fetchone()

    return render_template('login.html',
                            title="Secure Login",
                            heading="Secure Login")


@app.route("/register", methods=['GET', 'POST'])
def register():
    create_db()

    minChars = 8
    maxChars = 25
    validPass = True

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        pw_hash = hash_pw(password)

        # check for sql code in the register inputs
        sqlInjectionFound = False
        i = 0
        j = 0
        while i < len(blackList):
            if blackList[i] in username:
                errorMessage = "An SQL term has been detected, the website will now crash."
                print(errorMessage)
                sqlInjectionFound = True
            i = i + 1

        while j < len(blackList):
            if blackList[j] in password:
                errorMessage = "An SQL term has been detected, the website will now crash."
                print(errorMessage)
                sqlInjectionFound = True
            j = j + 1

        if sqlInjectionFound:
            redirect(url_for('register.html'))

        print("Trying user: " + username + " and pass: " + password)

        #checks for at least 1 upper case, 1 lower case, 1 digit
        if ( not any(x.isupper() for x in password) or not any(x.islower() for x in password)
                or not any(x.isdigit() for x in password)):
            validPass = False

        #checks that length is good
        if len(password) < minChars or len(password) > maxChars:
            validPass = False

        specialChars = ["?", "!", "#", "$", "%", "&", "*"]
        specialCharLocated = 0
        #checks for special chars
        for x in password:
            for y in specialChars:
                if x == y:
                    print("found special char")
                    specialCharLocated = 1

        if specialCharLocated == 0:
            validPass = False

        try:
            if validPass:
                addUser(username, password)
                print("added user...")
                flash("Successfully created new account.")
            else:
                flash("Invalid username or password!", 'alert-danger')
                print("invalid pass detected...")

        except KeyError:
            pass
            flash("Invalid username or password!", 'alert-danger')

    return render_template('register.html',
                           title="Secure Login",
                           heading="Secure Login")

@app.route("/login_success", methods=['GET', 'POST'])
def login_success():
    # flash("Welcome! You have logged in!", 'alert-success')
    return render_template('customerHomeLevel1.html',
                           title="Customer Home",
                           heading="Customer Home",
                           username = correctUserName,
                           accessLevel = accessLevel)

@app.route("/not_login_success", methods=['GET', 'POST'])
def not_login_success():
    return render_template('not_login_success.html')


@app.route("/createPassword", methods=['GET', 'POST'])
def generateStrongPassword():
    newPassword = getRandomPassword(25)
    return render_template('createPassword.html', generatedPassword = newPassword)

@app.route("/maxAttemptsReached", methods=['GET', 'POST'])
def maxLogins():
    return render_template('maxAttemptsReached.html')


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)