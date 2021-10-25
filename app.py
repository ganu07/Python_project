from flask import Flask, render_template,request, session, redirect, url_for
import requests
from flask_mail import *
from random import *
from twilio.rest import Client
from pdf_mail import sendpdf
from config import *
import pdfkit

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



@app.route("/", methods=["GET","POST"])
def login():
    msg = ' '
    if request.method == 'POST':
        global username, email1
        username = request.form['username']
        password = request.form['password']

        cursor.execute("select * from student_info where stu_name=%s and stu_pass=%s", (username, password))
        result = cursor.fetchone()
        if result:
            session['login'] = True
            session['username'] = result[1]
            email1 = result[3]
            session['phone'] = result[4]
            msg = "Choose your authorization method"
            return render_template("otp.html", username=session['username'], msg = msg)
        else:
            msg = 'username/password Not valid'
    return render_template("login.html", msg=msg)


@app.route('/email', methods = ["POST"])
def email():
    msg = "Enter your email address for OTP validation: "
    return render_template('email.html', email1 = session['email1'], username=session['username'], msg=msg)


@app.route('/verify',methods = ["POST"])
def verify():
    global email
    email = request.form["email"]
    msg = Message('OTP',sender = 'resultdetails364@gmail.com', recipients = [email])
    msg.body = str(otp)
    mail.send(msg)
    return render_template('verify.html')


@app.route('/phone', methods = ["POST"])
def phone():
    msg = "Enter your phone number for OTP validation: "
    return render_template('phone.html', phone = session['phone'], username=session['username'], msg=msg)


@app.route('/verify_phone',methods = ["POST"])
def verify_phone():
    number = request.form['number']
    if number.isdigit() and len(number) == 10:
        url = "https://www.fast2sms.com/dev/bulk"
        # account_sid = 'AC6cca1a96dbb79a974b68e98379880d88'
        # auth_token = '68d7e700063bbd625ae00c12523ab95b'
        # client = Client(account_sid, auth_token)
        body = 'your otp for result is : ' + str(otp)
        session['response'] = str(otp)
        payload = f"sender_id=FSTSMS&message={body}&language=english&route=p&numbers={number}"
        # message = client.messages.create(messaging_service_sid='MG02685050e5546d702d7a126357d64c4a',
        #                                  body=body,
        #                                  to=number)

        headers = {
            'authorization': "3uOilP4bhHc7SG512dQtIATao0ErmyZ8wxXeFfWsRvkNUBCVg6n7kU5rjlabEcOiqPd0gGQwYILFJxtz",
            'Content-Type': "application/x-www-form-urlencoded"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        if response :
            return render_template('verify_phone.html')
    else:
        msg1 = "Invalid phone number"
        return render_template("phone.html", msg1=msg1)


@app.route('/validate',methods=["POST"])
def validate():
    user_otp = request.form['otp']
    if user_otp.isdigit():
        if otp == int(user_otp):
            headings = ("emailid", "python", "java", "C", "javascript", "percent", "result")
            cursor.execute("select student_info.stu_email, student_result.python, student_result.java, " \
                  "student_result.c, student_result.javascript, student_result.percent, " \
                  "student_result.result from student_info inner join " \
                  "student_result on student_info.stu_id = student_result.stu_id where stu_name=%s", (username,))
            result = cursor.fetchall()
            rendered = render_template('example.html', headings=headings, result=result, username=username)
            pdf = pdfkit.from_string(rendered, False)
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Contecnt-Disposition'] = 'inline; filename=output.pdf'
            if email != email1:
                msg = Message('result_pdf', sender='resultdetails364@gmail.com', recipients=[email])
                msg.body = "Your result"
                msg.attach("result", "application/pdf", pdf)
                mail.send(msg)

            msg = Message('result_pdf', sender='resultdetails364@gmail.com', recipients=[email1])
            msg.body = "Your result"
            msg.attach("result", "application/pdf", pdf)
            mail.send(msg)

            return response
    msg="Invalid OTP"
    return render_template("verify.html", msg=msg)



if __name__ == '__main__':
    app.run(debug = True)