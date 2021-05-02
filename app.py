# importing helper libraries
from flask import Flask, render_template, url_for, flash, redirect, request, session, jsonify, send_file, Response
from rapidapi import str_rev_api, translate_api, weather_api, insta_api
from utils import *
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import ast
import json
import time
from time import sleep
from request_handlers import *
import os
from dotenv import load_dotenv
from curr_time import get_curr_time

load_dotenv()

MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

# import mysql.connector
# from mysql.connector.constants import ClientFlag

# setting up a flask app
app = Flask(__name__)

# random secret key
app.secret_key = ';\x01\x03A\x7f\x1d\xa8\x9e\x06\xf3\xf2m\x10"\xea\x99\x97\'\xf3\xc3\x0fQa\xbc'

# mail server connection
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = str(MAIL_USERNAME)
app.config['MAIL_PASSWORD'] = str(MAIL_PASSWORD)
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

reqID = 0

sleep(12)
# DATABASE CONNECTION
##GCP
# config = {
#     'user': 'root',
#     'password': 'root',
#     'host': '35.192.77.35',
#     'database': 'ESB',
#     'client_flags': [ClientFlag.SSL],
#     'ssl_ca': 'ssl/server-ca.pem',
#     'ssl_cert': 'ssl/client-cert.pem',
#     'ssl_key': 'ssl/client-key.pem'
# }
# cnxn = mysql.connector.connect(**config)

##LOCAL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = str(MYSQL_PASSWORD)
app.config['MYSQL_DB'] = str(MYSQL_DB)

mysql = MySQL(app)

# Admin Credentials : FIXED
admin = {}
admin["username"] = str(ADMIN_USERNAME)
admin["password"] = str(ADMIN_PASSWORD)

bcrypt = Bcrypt(app)
# ROUTES


# very first page of the ESB - login for admins
@app.route("/", methods=['GET', 'POST'])
def welcome_admin():
    print("hello")
    # if the cookies for username are already set then the user will be redirected to his/her dashboard
    # if s/he is admin
    if "username" in session and session["username"] == admin["username"]:
        return redirect(url_for('admin_dashboard'))

    # if s/he is user
    if "username" in session:
        return redirect(url_for('user_dashboard',
                                username=session["username"]))

    # if no cookies are there, then we'll wait for user to post the details
    if request.method == 'POST':
        # matching the values
        if request.form["username"] == admin["username"] and request.form[
                "password"] == admin["password"]:
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
        cursor = mysql.connection.cursor()
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
        cursor = mysql.connection.cursor()
        # selecting that particular users username, password and role
        cursor.execute('select * from SignupConfirmation where username = %s',
                       (str(username), ))
        user = cursor.fetchall()
        password = user[0][1]
        role = user[0][2]
        email = user[0][3]
        # finding priority of the user based on his/her role
        priority = find_priority(role)

        flag = True
        try:
            # sending mail for confirmation
            msg = Message('User Confirmation',
                          sender='cs305esb@gmail.com',
                          recipients=[str(email)])
            msg.body = "You are confirmed as a user on our ESB server. Now, you can login using the registered credentials."
            x = mail.send(msg)
            print("ddhg", x)
        except SMTPException:
            # mail sending failed - main does not exists that means - the user must be deleted
            flag = False

        cursor = mysql.connection.cursor()
        # deleting the user from SignupConfirmation table
        cursor.execute('DELETE from SignupConfirmation where username = %s',
                       (str(username), ))

        # commit all results in database
        mysql.connection.commit()

        if (flag):
            cursor = mysql.connection.cursor()
            # inserting the confirmed user in Users table
            cursor.execute(
                'INSERT into Users(Username,UserPassword,UserRole,UserPriority,Email) values(%s,%s,%s,%s,%s)',
                (str(username), str(password), str(role), priority,
                 str(email)))
            # commit
            mysql.connection.commit()

        # page is refreshed and the confirmed user's name will be removed from pending cofirmations list
        return redirect(url_for('admin_dashboard'))
    else:
        # if not a admin, then redirected to login page
        return redirect(url_for("welcome_admin"))


# for not confirming or deleting the user from confirmation table -- only admins can do this
@app.route("/delete_user/<username>", methods=['GET', 'POST'])
def delete_user(username):
    if "username" in session and session["username"] == admin["username"]:
        # declaring cursor for database connection cnxn
        cursor = mysql.connection.cursor()
        # selecting that particular users username, password and role
        cursor.execute('select * from SignupConfirmation where username = %s',
                       (str(username), ))
        user = cursor.fetchall()
        email = user[0][3]

        cursor = mysql.connection.cursor()
        # simply deleting the user and committing the changes
        cursor.execute('DELETE from SignupConfirmation where username = %s',
                       (str(username), ))
        mysql.connection.commit()
        # sending mail for rejection
        try:
            msg = Message('User Confirmation',
                          sender='cs305esb@gmail.com',
                          recipients=[str(email)])
            msg.body = "You are confirmed as a user on our ESB server. Now, you can login using the registered credentials."
            mail.send(msg)
        except:
            print("Email did not exist anyway.")
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
        return render_template("user_dashboard.html", username=username)
    # if no cookies are there for username then first redirect to user login page
    else:
        return redirect(url_for('user_login'))


# route for facilitating user login
@app.route("/user_login", methods=['GET', 'POST'])
def user_login():
    # if the user has already logged in
    if "username" in session and session["username"] != admin["username"]:
        # redirect her/him to her/his dashboard
        return redirect(url_for('user_dashboard',
                                username=session["username"]))

    # if not pre logged in
    if request.method == 'POST':
        # collect the username and passwd
        username = request.form["username"]
        passwd = request.form["password"]

        cursor = mysql.connection.cursor()
        # check if database contain such user
        cursor.execute('select * from Users where username = %s',
                       (str(username), ))
        user = cursor.fetchall()

        # if no such users -> invalid credentials -> login again
        print(len(user))
        if (len(user) == 0):
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
        return redirect(url_for('user_dashboard',
                                username=session["username"]))

    cursor = mysql.connection.cursor()
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
        email = request.form["email"]
        cursor = mysql.connection.cursor()
        # inserting the user data in SignupConfirmation table
        cursor.execute(
            'INSERT into SignupConfirmation(Username,UserPassword,UserRole,Email) values(%s,%s,%s,%s)',
            (username, passwd, role, email))
        # committing the changes
        mysql.connection.commit()

    return render_template("user_signup.html", unames=unames)


# route for logging out
@app.route("/logout")
def logout():
    # clear the cookie for username
    session.pop('username', None)
    return redirect(url_for("welcome_admin"))


# ROUTES FOR API CALLS
## string reverse API


@app.route("/string_reverse", methods=['GET', 'POST'])
def string_reverse():
    filename = ""
    if "username" in session and session["username"] == admin["username"]:
        filename = "base1.html"
    elif "username" in session and session["username"] != admin["username"]:
        filename = "base2.html"
    else:
        return redirect(url_for("welcome_admin"))
    out = "Output will be shown here."
    if request.method == 'POST':
        out = "sfdf"
        global reqID
        local_reqid = reqID+1
        
        string = request.form["string"]
        RequestSender(session["username"], "reverse", string, get_curr_time(),
                      local_reqid)
        out = check_update(local_reqid)
        # out = json_dict["reversed_string"]
        return render_template("string_reverse.html",
                               out=out,
                               filename=filename,
                               username=session["username"])
    return render_template("string_reverse.html",
                           out=out,
                           filename=filename,
                           username=session["username"])


# instagram API


@app.route("/instagram", methods=['GET', 'POST'])
def instagram():
    flag = 0
    filename = ""
    if "username" in session and session["username"] == admin["username"]:
        filename = "base1.html"
    elif "username" in session and session["username"] != admin["username"]:
        filename = "base2.html"
    else:
        return redirect(url_for("welcome_admin"))
    out = "Output will be shown here."
    if request.method == 'POST':
        out = []
        flag = 1
        string = request.form["string"]
        # this function is implemented in rapidapi.py file
        str_out = insta_api(string)
        json_dict = json.loads(str_out)
        if "status" in json_dict and json_dict["status"] == "fail":
            flag = 0
            out = "Oops! Profile not found"
            return render_template("insta.html",
                                   out=out,
                                   filename=filename,
                                   username=session["username"],
                                   flag=flag)
        bio = json_dict["biography"]
        followers = json_dict["edge_followed_by"]["count"]
        following = json_dict["edge_follow"]["count"]
        out = [bio, followers, following]
        return render_template("insta.html",
                               out=out,
                               filename=filename,
                               username=session["username"],
                               flag=flag)
    return render_template("insta.html",
                           out=out,
                           filename=filename,
                           username=session["username"],
                           flag=flag)


# weather API


@app.route("/weather", methods=['GET', 'POST'])
def weather():
    filename = ""
    if "username" in session and session["username"] == admin["username"]:
        filename = "base1.html"
    elif "username" in session and session["username"] != admin["username"]:
        filename = "base2.html"
    else:
        return redirect(url_for("welcome_admin"))
    out = "Output will be shown here."
    flag = 0
    if request.method == 'POST':
        flag = 1
        string = request.form["string"]
        # this function is implemented in rapidapi.py file
        str_out = weather_api(string)
        if (str_out[0] == 't'):
            str_out = str_out[4:]
        else:
            out = "Oops! City not found"
            flag = 0
            return render_template("weather.html",
                                   out=out,
                                   filename=filename,
                                   username=session["username"],
                                   flag=flag)
        json_dict = ast.literal_eval(str_out)
        out = []
        out.append(json_dict["weather"][0]["main"])
        out.append(json_dict["weather"][0]["description"])
        out.append(json_dict["main"]["temp"])
        out.append(json_dict["main"]["feels_like"])
        out.append(json_dict["main"]["temp_min"])
        out.append(json_dict["main"]["temp_max"])
        out.append(json_dict["main"]["pressure"])
        out.append(json_dict["main"]["humidity"])
        return render_template("weather.html",
                               out=out,
                               filename=filename,
                               username=session["username"],
                               flag=flag)
    return render_template("weather.html",
                           out=out,
                           filename=filename,
                           username=session["username"],
                           flag=flag)


# Google Translate API
@app.route("/translator", methods=['GET', 'POST'])
def translator():
    filename = ""
    if "username" in session and session["username"] == admin["username"]:
        filename = "base1.html"
    elif "username" in session and session["username"] != admin["username"]:
        filename = "base2.html"
    else:
        return redirect(url_for("welcome_admin"))
    out = "Output will be shown here."
    flag = 0
    if request.method == 'POST':
        out = []
        flag = 1
        string = request.form["string"]
        # this function is implemented in rapidapi.py file
        str_out = translate_api(string)
        json_dict = json.loads(str_out)
        lang_code = json_dict["data"]["detections"][0][0]["language"]
        confidence = json_dict["data"]["detections"][0][0]["confidence"]
        lang_name = ""
        f = open('static/languages_codes.json')
        data = json.load(f)
        for i in data["code2lang"]:
            if (i["alpha2"] == lang_code):
                lang_name = i["English"]
                break
        out.append(lang_name)
        out.append(confidence)
        return render_template("detect.html",
                               out=out,
                               filename=filename,
                               username=session["username"],
                               flag=flag)
    return render_template("detect.html",
                           out=out,
                           filename=filename,
                           username=session["username"],
                           flag=flag)


@app.route('/client2client', methods=['GET', 'POST'])
def client2client():
    filename = ""
    if "username" in session and session["username"] == admin["username"]:
        filename = "base1.html"
    elif "username" in session and session["username"] != admin["username"]:
        filename = "base2.html"
    else:
        return redirect(url_for("welcome_admin"))
    out = "Output will be shown here."
    global reqID
    reqID += 1
    online_users = get_users()
    if request.method == 'POST':
        username = request.form["string"]
        if username not in online_users:
            out = "There's no user with username " + username
        else:
            message = request.form["message"]
            curr_timestamp = time.time()
            out = C2CHandler(session["username"], username, message,
                             curr_timestamp, reqID)
            return render_template("client2client.html",
                                   online_users=online_users,
                                   out=out,
                                   filename=filename,
                                   username=session["username"])
    return render_template("client2client.html",
                           online_users=online_users,
                           out=out,
                           filename=filename,
                           username=session["username"])


# for a particular requesID the client will ping this route to check for any available updates
def check_update(ID):
    cursor = mysql.connection.cursor()
    for i in range(0,15):
        time.sleep(0.5)
        cursor.execute("SELECT Response from AckLogs where RequestID = %s",(ID,))
        if cursor.rowcount > 0:
            out = cursor.fetchall()[0][0]
            return out
    out = "OOPS! Request Timed Out"


def get_users():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT username from Users')
    mysql.connection.commit()
    users = cursor.fetchall()
    final_users = []
    for user in users:
        final_users.append(user[0])
    return final_users


# starting the APP
if __name__ == '__main__':
    app.run(debug=True)