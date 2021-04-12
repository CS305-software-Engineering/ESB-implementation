# importing helper libraries
from flask import Flask, render_template, url_for, flash, redirect, request, session, jsonify, send_file, Response
from rapidapi import str_rev_api, translate_api, weather_api, insta_api
from utils import *
import bcrypt
import mysql.connector
from mysql.connector.constants import ClientFlag

# setting up a flask app
app = Flask(__name__)
# random secret key
app.secret_key = ';\x01\x03A\x7f\x1d\xa8\x9e\x06\xf3\xf2m\x10"\xea\x99\x97\'\xf3\xc3\x0fQa\xbc'

# DATABASE CONNECTION 
config = {
    'user': 'root',
    'password': 'root',
    'host': '35.192.77.35',
    'database': 'ESB',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'ssl/server-ca.pem',
    'ssl_cert': 'ssl/client-cert.pem',
    'ssl_key': 'ssl/client-key.pem'
}
cnxn = mysql.connector.connect(**config)

# Admin Credentials : FIXED
admin = {} 
admin["username"] = "admin"
admin["password"] = "pass123"

# ROUTES 

# very first page of the ESB - login for admins
@app.route("/", methods=['GET', 'POST'])
def welcome_admin():
    # if the cookies for username are already set then the user will be redirected to his/her dashboard 
    # if s/he is admin
    if "username" in session and session["username"] == admin["username"]:
        return redirect(url_for('admin_dashboard'))

    # if s/he is user
    if "username" in session:
        return redirect(url_for('user_dashboard',username=session["username"]))

    # if no cookies are there, then we'll wait for user to post the details
    if request.method == 'POST':
        # matching the values
        if request.form["username"] == admin["username"] and request.form["password"] == admin["password"]:
            # if matched, set cookies and redirect
            session["username"] = admin["username"]
            return redirect(url_for('admin_dashboard'))
    # if invalid, redirection to the same page will occur
    return render_template("admin_login.html")

# route for admin dashboard
@app.route("/admin", methods=['GET', 'POST'])
def admin_dashboard():
    # the user will be able to access the contents of this page only if the username cookie has the value equal to admin's username
    if "username" in session and session["username"] == admin["username"]:
        # declaring cursor for database connection cnxn
        cursor = cnxn.cursor()
        # selecting all users from SignUpConfirmation table and storing them in pending_users list
        cursor.execute('select * from SignupConfirmation')
        pending_users = cursor.fetchall()

        # fetching all logs from AckLogs table so that they can be shown on admin dashboard
        cursor.execute("SELECT * from AckLogs")
        logs = cursor.fetchall()

        # rendering the template with required values
        return render_template("admin_dashboard.html",
                                logs=logs,
                                n=len(logs),
                                pending_users=pending_users,
                                m=len(pending_users))
        
    # if no cookies, redirect to admin login page
    else:
        return redirect(url_for("welcome_admin"))

# route to confirm a user -- only admins can do this
@app.route("/confirm_user/<username>", methods=['GET', 'POST'])
def confirm_user(username):
    # checking if the current user is admin
    if "username" in session and session["username"] == admin["username"]:
        # declaring cursor for database connection cnxn
        cursor = cnxn.cursor()
        # selecting that particular users username, password and role
        cursor.execute('select * from SignupConfirmation where username = %s',(str(username), ))
        user = cursor.fetchall()

        cursor = cnxn.cursor()
        # deleting the user from SignupConfirmation table 
        cursor.execute('DELETE from SignupConfirmation where username = %s',(str(username), ))
        
        # commit all results in database
        cnxn.commit()

        password = user[0][1]
        role = user[0][2]
        # finding priority of the user based on his/her role
        priority = find_priority(role)

        cursor = cnxn.cursor()
        # inserting the confirmed user in Users table
        cursor.execute('INSERT into Users(Username,UserPassword,UserRole,UserPriority) values(%s,%s,%s,%s)',(str(username), str(password), str(role), priority))
        # commit 
        cnxn.commit()
        
        # page is refreshed and the confirmed user's name will be removed from pending cofirmations list
        return redirect(url_for('admin_dashboard'))
    else:
        # if not a admin, then redirected to login page
        return redirect(url_for("welcome_admin"))

# for not confirming or deleting the user from confirmation table -- only admins can do this
@app.route("/delete_user/<username>", methods=['GET', 'POST'])
def delete_user(username):
    if "username" in session and session["username"] == admin["username"]:
        cursor = cnxn.cursor()
        # simply deleting the user and committing the changes
        cursor.execute('DELETE from SignupConfirmation where username = %s',(str(username), ))
        cnxn.commit()
        # page is refreshed and the deleted user's name will be removed from pending cofirmations list
        return redirect(url_for('admin_dashboard'))
    else:
        # if not a admin, then redirected to login page
        return redirect(url_for("welcome_admin"))

# displaying user dashboard of a particular user
@app.route("/user_dashboard/<username>")
def user_dashboard(username):
    # if that user is not admin 
    if "username" in session and session["username"] != admin["username"]:
        return render_template("user_dashboard.html",username=username)
    # if no cookies are there for username then first redirect to user login page
    else:
        return redirect(url_for('user_login'))

# route for facilitating user login
@app.route("/user_login", methods=['GET', 'POST'])
def user_login():
    # if the user has already logged in
    if "username" in session and session["username"] != admin["username"]:
        # redirect her/him to her/his dashboard
        return redirect(url_for('user_dashboard', username=session["username"]))
    
    # if not pre logged in 
    if request.method == 'POST':
        # collect the username and passwd
        username = request.form["username"]
        passwd = request.form["password"]

        cursor = cnxn.cursor()
        # check if database contain such user 
        cursor.execute('select * from Users where username = %s',(str(username), ))
        user = cursor.fetchall()

        # if no such users -> invalid credentials -> login again
        if(user.count == 0):
            return redirect(url_for('user_login'))
        
        # else check if passwd matches or not
        if bcrypt.check_password_hash(user[0][1], passwd):
            # if yes then set the cookies and redirect to dashboard
            session["username"] = username
            return redirect(url_for('user_dashboard', username=username))
        # else ask to login again with correct credentials
        else:
            return redirect(url_for('user_login'))
    return render_template("user_login.html")

# route for user signup
@app.route("/user_signup", methods=['GET', 'POST'])
def user_signup():
    # if the user has already logged in
    if "username" in session and session["username"] != admin["username"]:
        # redirect her/him to her/his dashboard
        return redirect(url_for('user_dashboard', username=session["username"]))
    
    cursor = cnxn.cursor()
    # collecting all the existing usernames in unames list till now, so that the new user should not be allowed to use the same username ( usernames are unique )
    cursor.execute('SELECT username from SignupConfirmation')
    uname1 = cursor.fetchall()
    cursor.execute('SELECT * from Users')
    uname2 = cursor.fetchall()
    unames = []

    for val in uname1:
        unames.append(val[0])
    for val in uname2:
        unames.append(val[0])

    if request.method == 'POST':
        # storing form data on POST
        username = request.form["username"]
        passwd = bcrypt.generate_password_hash(request.form["password"]) 
        role = request.form["role"]
        cursor = cnxn.cursor()
        # inserting the user data in SignupConfirmation table
        cursor.execute('INSERT into SignupConfirmation(Username,UserPassword,UserRole) values(%s,%s,%s)',(username, passwd, role))
        # committing the changes
        cnxn.commit()

    return render_template("user_signup.html", unames=unames)

# route for logging out
@app.route("/logout")
def logout():
    # clear the cookie for username
    session.pop('username',None) 
    return redirect(url_for("welcome_admin"))    
    
# ROUTES FOR API CALLS
## string reverse API

@app.route("/string_reverse", methods=['GET', 'POST'])
def string_reverse():
    out = "Output will be shown here."
    if request.method == 'POST':
        string = request.form["string"]
        # this function is implemented in rapidapi.py file
        out = str_rev_api(string) 
        return render_template("string_reverse.html", out=out)
    return render_template("string_reverse.html", out=out)

# instagram API

@app.route("/instagram", methods=['GET', 'POST'])
def instagram():
    out = "Output will be shown here."
    if request.method == 'POST':
        string = request.form["string"]
        # this function is implemented in rapidapi.py file
        out = insta_api(string)
        return render_template("insta.html", out=out)
    return render_template("insta.html", out=out)

# weather API

@app.route("/weather", methods=['GET', 'POST'])
def weather():
    out = "Output will be shown here."
    if request.method == 'POST':
        string = request.form["string"]
        # this function is implemented in rapidapi.py file
        out = weather_api(string)
        return render_template("weather.html", out=out)
    return render_template("weather.html", out=out)

# Google Translate API
@app.route("/translator", methods=['GET', 'POST'])
def translator():
    out = "Output will be shown here."
    if request.method == 'POST':
        string = request.form["string"]
        # this function is implemented in rapidapi.py file
        out = translate_api(string)
        return render_template("detect.html", out=out)
    return render_template("detect.html", out=out)

# starting the APP
if __name__ == '__main__':
    app.run(debug=True)