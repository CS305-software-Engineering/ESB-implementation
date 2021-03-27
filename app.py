from flask import Flask,render_template,url_for,flash,redirect,request,session ,jsonify,send_file,Response
from flask_sqlalchemy import SQLAlchemy

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
    if request.method == 'POST':
        string = request.form["string"]
    return render_template("string_reverse.html")
    
    
if __name__=='__main__':
    app.run(debug=True)