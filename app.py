from flask import Flask,render_template,url_for,flash,redirect,request,session ,jsonify,send_file,Response
from flask_sqlalchemy import SQLAlchemy
from rapidapi import str_rev_api,translate_api,weather_api,insta_api
app = Flask(__name__)
# 'mysql://username:password@localhost/dbname'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://postgres:iamstillworthy@localhost/esb'
db = SQLAlchemy(app)

admin = {}
admin["username"] = "admin"
admin["password"] = "pass123"

@app.route("/",methods=['GET','POST'])
def welcome_admin():
    if request.method == 'POST':
        if request.form["username"] == admin["username"] and request.form["password"] == admin["password"]:
            return redirect(url_for('admin_dashboard'))
    return render_template("admin_login.html")

@app.route("/admin",methods=['GET','POST'])
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/user_login")
def user_login():
    
    return render_template("user_login.html")

@app.route("/user_signup")
def user_signup():
    return render_template("user_signup.html")
    
@app.route("/string_reverse", methods=['GET','POST'])
def string_reverse():
    out = "Output will be shown here."
    if request.method == 'POST':
        string = request.form["string"]
        out = str_rev_api(string)
        return render_template("string_reverse.html",out = out)
    return render_template("string_reverse.html",out = out)
    
@app.route("/instagram", methods=['GET','POST'])
def instagram():
    out = "Output will be shown here."
    if request.method == 'POST':
        string = request.form["string"]
        out = insta_api(string)
        return render_template("insta.html",out = out)
    return render_template("insta.html",out = out)
    
@app.route("/weather", methods=['GET','POST'])
def weather():
    out = "Output will be shown here."
    if request.method == 'POST':
        string = request.form["string"]
        out = weather_api(string)
        return render_template("weather.html",out = out)
    return render_template("weather.html",out = out)

@app.route("/translator", methods=['GET','POST'])
def translator():
    out = "Output will be shown here."
    if request.method == 'POST':
        string = request.form["string"]
        out = translate_api(string)
        return render_template("detect.html",out = out)
    return render_template("detect.html",out = out)

if __name__=='__main__':
    app.run(debug=True)