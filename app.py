from flask import Flask, render_template,request, session, redirect, flash
from flask_mail import *
from random import *
from twilio.rest import Client
import mysql.connector
from config import *
import sys

app = Flask(__name__)
app.secret_key = "super secret key"


mail = Mail(app)
app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'resultdetails364@gmail.com'
app.config['MAIL_PASSWORD'] = 'Ganesh@123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


otp = randint(000000,999999)

@app.route('/login')
def index():
    return render_template('login.html')

@app.route('/email', methods = ["POST"])
def email():
    return render_template('email.html')

@app.route('/phone', methods = ["POST"])
def phone():
    return render_template('phone.html')

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            cursor = mydb.cursor()
            cursor.execute("select * from student_info where stu_name=%s and stu_pass=%s", (username, password))
            result = cursor.fetchone()
            if result is not None:
                # if result['username'] == username and result['password'] == password:
                return render_template('otp.html')
            else:
                flash("username or password incorrect", category='failure')
                return render_template("login.html")
    return render_template("login.html")


@app.route('/verify',methods = ["POST"])
def verify():
    email = request.form["email"]
    msg = Message('OTP',sender = 'resultdetails364@gmail.com', recipients = [email])
    msg.body = str(otp)
    mail.send(msg)
    return render_template('verify.html')

@app.route('/verify_phone',methods = ["POST"])
def verify_phone():
    number = request.form['number']
    account_sid = 'AC6cca1a96dbb79a974b68e98379880d88'
    auth_token = '68d7e700063bbd625ae00c12523ab95b'
    client = Client(account_sid, auth_token)
    body = 'your otp is' + str(otp)
    session['response'] = str(otp)
    message = client.messages.create(messaging_service_sid='MG02685050e5546d702d7a126357d64c4a', body=body, to=number)
    if message.sid :
        return render_template('verify_phone.html')

@app.route('/validate',methods=["POST"])
def validate():
    user_otp = request.form['otp']
    if otp == int(user_otp):
        return "<h3> OTP verification is  successful </h3>"
    return "<h3>failure, OTP does not match</h3>"


if __name__ == '__main__':
    app.run(debug = True)