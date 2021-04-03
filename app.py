from flask import Flask, render_template, url_for, flash, redirect, request, session, jsonify, send_file, Response
from rapidapi import str_rev_api, translate_api, weather_api, insta_api
from utils import *
import mysql.connector
from mysql.connector.constants import ClientFlag

app = Flask(__name__)

#### DATABASE CONNECTION PART######
config = {'user': 'root', 'password': 'root', 'host': '35.192.77.35', 'database': 'ESB', 'client_flags': [
    ClientFlag.SSL], 'ssl_ca': 'ssl/server-ca.pem', 'ssl_cert': 'ssl/client-cert.pem', 'ssl_key': 'ssl/client-key.pem'}

cnxn = mysql.connector.connect(**config)
#####################################
admin = {}
admin["username"] = "admin"
admin["password"] = "pass123"


@app.route("/", methods=['GET', 'POST'])
def welcome_admin():
    if "username" in session and session["username"] == admin["username"]:
        return redirect(url_for('admin_dashboard'))

    if "username" in session:
        return redirect(url_for('user_dashboard', username=session["username"]))

    if request.method == 'POST':
        if request.form["username"] == admin["username"] and request.form[
                "password"] == admin["password"]:
            session["username"] = admin["username"]
            return redirect(url_for('admin_dashboard'))
    return render_template("admin_login.html")


@app.route("/admin", methods=['GET', 'POST'])
def admin_dashboard():
    if "username" in session and session["username"] == admin["username"]:
        cursor = cnxn.cursor()
        cursor.execute('select * from SignupConfirmation')
        pending_users = cursor.fetchall()

        cursor.execute("SELECT * from AckLogs")
        logs = cursor.fetchall()

        print(pending_users)
        return render_template("admin_dashboard.html", logs=logs, n=len(logs), pending_users=pending_users, m=len(pending_users))
    else:
        return redirect(url_for("welcome_admin"))


@app.route("/confirm_user/<username>", methods=['GET', 'POST'])
def confirm_user(username):
    if "username" in session and session["username"] == admin["username"]:
        cursor = cnxn.cursor()
        cursor.execute(
            'select * from SignupConfirmation where username = %s', (str(username),))
        user = cursor.fetchall()
        print(user)

        cursor = cnxn.cursor()
        cursor.execute(
            'DELETE from SignupConfirmation where username = %s', (str(username),))
        cnxn.commit()
        print(cursor.rowcount)

        password = user[0][1]
        role = user[0][2]
        priority = find_priority(role)

        cursor = cnxn.cursor()
        cursor.execute('INSERT into Users(Username,UserPassword,UserRole,UserPriority) values(%s,%s,%s,%s)', (str(
            username), str(password), str(role), priority))
        cnxn.commit()
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for("welcome_admin"))


@app.route("/user_dashboard/<username>")
def user_dashboard(username):
    if "username" in session and session["username"] != admin["username"]:
        return render_template("user_dashboard.html")
    else:
        return redirect(url_for('user_login'))


@app.route("/user_login", methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form["username"]
        passwd = request.form["password"]

        cursor = cnxn.cursor()
        cursor.execute(
            'select * from Users where username = %s', (str(username),))
        user = cursor.fetchall()

        if user[0][1] == passwd:
            session["username"] = username
            return redirect(url_for('user_dashboard', username=username))
        else:
            return redirect(url_for('user_login'))
    return render_template("user_login.html")


@app.route("/user_signup", methods=['GET', 'POST'])
def user_signup():
    cursor = cnxn.cursor()
    cursor.execute('SELECT username from SignupConfirmation')
    uname1 = cursor.fetchall()
    cursor.execute('SELECT * from Users')
    uname2 = cursor.fetchall()
    unames = []

    print(uname1)
    print(uname2)
    for val in uname1:
        unames.append(val[0])
    for val in uname2:
        unames.append(val[0])

    if request.method == 'POST':
        username = request.form["username"]
        passwd = request.form["password"]
        role = request.form["role"]
        cursor = cnxn.cursor()
        cursor.execute(
            'INSERT into SignupConfirmation(Username,UserPassword,UserRole) values(%s,%s,%s)', (username, passwd, role))
        cnxn.commit()

    return render_template("user_signup.html", unames=unames)


@app.route("/string_reverse", methods=['GET', 'POST'])
def string_reverse():
    out = "Output will be shown here."
    if request.method == 'POST':
        string = request.form["string"]
        out = str_rev_api(string)
        return render_template("string_reverse.html", out=out)
    return render_template("string_reverse.html", out=out)


@app.route("/instagram", methods=['GET', 'POST'])
def instagram():
    out = "Output will be shown here."
    if request.method == 'POST':
        string = request.form["string"]
        out = insta_api(string)
        return render_template("insta.html", out=out)
    return render_template("insta.html", out=out)


@app.route("/weather", methods=['GET', 'POST'])
def weather():
    out = "Output will be shown here."
    if request.method == 'POST':
        string = request.form["string"]
        out = weather_api(string)
        return render_template("weather.html", out=out)
    return render_template("weather.html", out=out)


@app.route("/translator", methods=['GET', 'POST'])
def translator():
    out = "Output will be shown here."
    if request.method == 'POST':
        string = request.form["string"]
        out = translate_api(string)
        return render_template("detect.html", out=out)
    return render_template("detect.html", out=out)


if __name__ == '__main__':
    app.run(debug=True)
