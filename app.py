from flask import Flask, render_template,request, session, redirect, url_for
import requests
from flask_mail import *
from random import *
from config import *
import pdfkit
import re

app = Flask(__name__)
app.secret_key = "super secret key"

app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'resultdetails364@gmail.com'
app.config['MAIL_PASSWORD'] = 'Ganesh@123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

otp = randint(000000,999999)
regex_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
regex_phone = '^[789]\d{9}$'
user_name = "^[a-z]+[a-z]$"


@app.route("/", methods=["GET", "POST"])
def login():
    msg = ' '

    if request.method == 'POST':
        global username, email1
        username = request.form['username']
        password = request.form['password']
        if re.search(user_name, username):
            cursor = mydb.cursor()
            cursor.execute("select * from student_info where stu_name=%s and stu_pass=%s", (username, password))
            result = cursor.fetchone()
            if result:
                session['login'] = True
                session['stu_id']= result[0]
                session['username'] = result[1]
                session['email1'] = result[3]
                session['phone'] = result[4]
                email1 = session['email1']
                msg = "Choose your authorization method"
                return render_template("otp.html", username=session['username'], msg=msg)
            else:
                msg = 'username/password Not valid'
        else:
            msg = 'username/password Not valid'
    return render_template("login.html", msg=msg)

@app.before_request
def make_session_permanent():
    session.permanent = True
    mydb.reconnect()

@app.route('/email', methods = ["POST"])
def email():
    msg = "Enter your email address for OTP validation: "
    return render_template('email.html', email1=session['email1'], username=session['username'], msg=msg)


@app.route('/verify',methods = ["POST"])
def verify():
    try:
        global email, number
        email = request.form["email"]
        number = 'abcd'
        if re.search(regex_email, email):
            msg = Message('TECHLEARN ACADAMY', sender='resultdetails364@gmail.com', recipients=[email])
            msg.body = f"Greetings from TECHLEARN ACADAMY! \n Hello {username}," \
                       "\nYour OTP for result is: " + str(otp)
            mail.send(msg)

            return render_template('verify.html')
        else:
            alet = "Invalid Email"
            return render_template('email.html', alet=alet)
    except:
        mydb.reconnect()
        msg = "something went wrong"
        return render_template("email.html", msg=msg)


@app.route('/phone', methods = ["POST"])
def phone():
    msg = "Enter your phone number for OTP validation: "
    return render_template('phone.html',phone = session['phone'], username=session['username'], msg=msg)


@app.route('/verify_phone',methods = ["POST"])
def verify_phone():
    try:
        global number
        number = request.form['number']
        try:
            if re.search(regex_phone, number):
                url = "https://www.fast2sms.com/dev/bulk"
                body = f"Greetings from TECHLEARN ACADAMY! \n Hello {username}," \
                           "\nYour OTP for result is: " + str(otp)
                session['response'] = str(otp)
                payload = f"sender_id=FSTSMS&message={body}&language=english&route=p&numbers={number}"
                headers = {
                    'authorization': "3uOilP4bhHc7SG512dQtIATao0ErmyZ8wxXeFfWsRvkNUBCVg6n7kU5rjlabEcOiqPd0gGQwYILFJxtz",
                    'Content-Type': "application/x-www-form-urlencoded"
                }
                response = requests.request("POST", url, data=payload, headers=headers)
                if response is not None:
                    return render_template('verify_phone.html')
                else:
                    return render_template('phone.html', msg="Invalid number")
            else:
                alet = "Invalid phone number! Please try again"
                return render_template("phone.html", alet=alet, username=session['username'])
        except Exception as e:
            mydb.reconnect()
            msg = "something went wrong"
            return render_template("phone.html", msg=msg)

    except :
        msg = "something went wrong"
        return render_template("phone.html", msg=msg)


@app.route('/validate',methods=["POST"])
def validate():
    try:
        user_otp = request.form['otp']
        if user_otp.isdigit():
            if otp == int(user_otp):
                headings = ("roll no", "python", "java", "C", "javascript", "percent", "result")
                cursor = mydb.cursor()
                cursor.execute("Select * from student_result where stu_id=%s", (session['stu_id'],))
                result = cursor.fetchall()
                rendered = render_template('example.html', headings=headings, result=result, username=username)
                pdf = pdfkit.from_string(rendered, False)
                response = make_response(pdf)
                response.headers['Content-Type'] = 'application/pdf'
                response.headers['Contecnt-Disposition'] = 'inline; filename=output.pdf'
                if number.isdigit():
                    msg = Message('result_pdf', sender='resultdetails364@gmail.com', recipients=[email1])
                    msg.body = f"Hey {username}, your result is follow:"
                    msg.attach("result", "application/pdf", pdf)
                    mail.send(msg)
                else:
                    msg = Message('result_pdf', sender='resultdetails364@gmail.com', recipients=[email])
                    msg.body = f"Hey {username}, your result is follow:"
                    msg.attach("result", "application/pdf", pdf)
                    mail.send(msg)
                return response
        msg="Invalid OTP"
        return render_template("verify.html", msg=msg)

    except:
        mydb.reconnect()
        msg = "something went wrong"
        return validate()

if __name__ == '__main__':
    app.run(debug = True)