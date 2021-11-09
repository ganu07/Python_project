import weasyprint
from flask import Flask, render_template,request, session, redirect, url_for
import requests
from flask_mail import *
from random import *
from config import *
import re
from flask_weasyprint import HTML
from flask_ngrok import run_with_ngrok

import os
import smtplib

app = Flask(__name__)
# run_with_ngrok(app)
app.secret_key = "super secret key"

app.config["MAIL_SERVER"]= 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'resultdetail7@gmail.com'
app.config['MAIL_PASSWORD'] = 'Ganesh@123'
#app.config['MAIL_USE_TLS'] = False
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
            cursor.close()
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
    mydb.connect()

@app.route('/email', methods = ["POST"])
def email():
    msg = "Enter your email address for OTP validation: "
    return render_template('email.html', email1=session['email1'], username=session['username'], msg=msg)


@app.route('/verify',methods = ["POST"])
def verify():
    try:
        global email
        email = request.form["email"]
        if re.search(regex_email, email):
            msg = Message('TECHLEARN ACADAMY', sender='resultdetails364@gmail.com', recipients=[email])
            msg.body = f"Greetings from TECHLEARN ACADAMY! \n Hello {username}," \
                       "\nYour OTP for result is: " + str(otp)
            mail.send(msg)

            return render_template('verify.html')
        else:
            alet = "Invalid Email"
            return render_template('email.html', alet=alet)
    except Exception:
        mydb.connect()
        msg = "something went wrong"
        return render_template("email.html", msg=msg)


@app.route('/phone', methods = ["POST"])
def phone():
    msg = "Enter your phone number for OTP validation and enter email id to receive Result: "
    return render_template('phone.html',phone = session['phone'], email1=session['email1'], username=session['username'], msg=msg)


@app.route('/verify_phone',methods = ["POST"])
def verify_phone():
    try:
        global email, number
        email = request.form["email"]
        number = request.form['number']
        if re.search(regex_phone, number) and re.search(regex_email, email):
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
            alet = "Invalid phone number or Email! Please try again"
            return render_template("phone.html", alet=alet, username=session['username'])
    except Exception:
        mydb.connect()
        msg = "something went wrong"
        return render_template("phone.html", msg=msg)


def html_to_pdf(html):
    htmldocs = HTML(string=html, base_url=" ")
    # pdf = htmldocs.write_pdf()
    # with open("in.pdf", "wb") as f:
    #     f.write(pdf)
    # out = PdfFileWriter()
    # file = PdfFileReader("in.pdf")
    # num = file.numPages8
    # for i in range(num):
    #     page = file.getPage(i)
    #     out.addPage(page)
    # with open("out.pdf", "wb") as f:
    #     out.write(f)
    return htmldocs.write_pdf()


@app.route('/validate',methods=["POST"])
def validate():
    mydb.connect()
    user_otp = request.form['otp']
    if otp == int(user_otp):
        headings = ("Email", "Python", "Java", "C", "Javascript", "Percent", "Result")
        cursor = mydb.cursor()
        cursor.execute("select student_info.stu_email, student_result.python, student_result.java, "
                       "student_result.c, student_result.javascript, student_result.percent, "
                       "student_result.result from student_info inner join " 
                       "student_result on student_info.stu_id = student_result.stu_id where stu_name=%s", (username,))
        result = cursor.fetchall()
        cursor.close()
        html = render_template('example.html', headings=headings, result=result, username=username)
        msg = Message('Techlearn Acadamy Result', sender='resultdetails364@gmail.com', recipients=[email])
        pdf = html_to_pdf(html)
        msg.body = f"Hello {username} , We have attached PDF copy of Result"
        msg.attach("result_{}".format(username) + '.pdf', 'application/pdf', pdf)
        mail.send(msg)
        return "Result has been sent Successfully!!!!"

    msg="Invalid OTP"
    return render_template("verify.html", msg=msg)


if __name__ == '__main__':
    app.run(debug=True)