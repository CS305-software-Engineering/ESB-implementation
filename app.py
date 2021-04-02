from flask import Flask, render_template, url_for, flash, redirect, request, session, jsonify, send_file, Response
from rapidapi import str_rev_api, translate_api, weather_api, insta_api
from utils import *
import mysql.connector
from mysql.connector.constants import ClientFlag

app = Flask(__name__)

#### DATABASE CONNECTION PART######
config = {'user': 'root', 'password': 'root', 'host': '35.192.77.35', 'database': 'ESB', 'client_flags': [ClientFlag.SSL], 'ssl_ca': 'ssl/server-ca.pem', 'ssl_cert': 'ssl/client-cert.pem', 'ssl_key': 'ssl/client-key.pem'}

cnxn = mysql.connector.connect(**config)
#####################################
admin = {}
admin["username"] = "admin"
admin["password"] = "pass123"


@app.route("/", methods=['GET', 'POST'])
def welcome_admin():
    if request.method == 'POST':
        if request.form["username"] == admin["username"] and request.form[
                "password"] == admin["password"]:
            return redirect(url_for('admin_dashboard'))
    return render_template("admin_login.html")


@app.route("/admin", methods=['GET', 'POST'])
def admin_dashboard():
    cursor = cnxn.cursor()
    cursor.execute('select * from SignupConfirmation')
    pending_users = cursor.fetchall()
    print(pending_users)
    return render_template("admin_dashboard.html",pending_users=pending_users,m=len(pending_users))

@app.route("/confirm_user/<username>", methods=['GET', 'POST'])
def confirm_user(username):
    cursor = cnxn.cursor()
    cursor.execute('select * from SignupConfirmation where username = %s',(str(username),))
    user = cursor.fetchall()
    print(user)
    
    cursor = cnxn.cursor()
    cursor.execute('DELETE from SignupConfirmation where username = %s',(str(username),))
    cnxn.commit()
    print(cursor.rowcount)
    
    
    password = user[0][1]
    role = user[0][2]
    priority = find_priority(role)
    
    cursor = cnxn.cursor()
    cursor.execute('INSERT into Users(Username,UserPassword,UserRole,UserPriority) values(%s,%s,%s,%s)', (str(username), str(password), str(role),priority))
    cnxn.commit()
    return redirect(url_for('admin_dashboard'))
    
@app.route("/user_login")
def user_login():

    return render_template("user_login.html")


@app.route("/user_signup", methods=['GET', 'POST'])
def user_signup():
    if request.method == 'POST':
        username = request.form["username"]
        passwd = request.form["password"]
        role = request.form["role"]
        cursor = cnxn.cursor()
        cursor.execute('INSERT into SignupConfirmation(Username,UserPassword,UserRole) values(%s,%s,%s)', (username, passwd, role))
        cnxn.commit()

    return render_template("user_signup.html")


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