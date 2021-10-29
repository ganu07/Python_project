# Python_project

OTP authorization via mobile number / email id to get result from the database.

FRONTEND:
  * HTML
  * JINJA Template
 
BACKEND:
   * SQL

FRAMEWORK:
  * Flask
  * python 
 
Modules:
  * requests
  * flask_mail
  * random
  * pdfkit
  * re

Description:

The project is specifically used to rettrive result from database and send the pdf copy of mail to user email

The project doesnt contain register/sign up page there is only login page because user/student is already present in database.
student/user have to login to proceed otp validation process. If username and password is correct then it will redirect to next
page which is otp validation page else user/student will get error messgae invalid username/password.

Once user/student in OTP validation page user have two option either via phone number or email id. If user/syudent choose
email then user have to enter email id or by deault it will take from database after submiting user will get OTP.
the page redirected to another page where user have to enter OTP. if OTP validation successfull then user will received mail of 
result pdf.

If user choose OTP varification via phone number then user will received OTP message and redirected to anothe page.
If OTP varification successfully done then user will received mail of result pdf to email id which is stored in database.


Future Improvement:
1) I will work on to download result in pdf as well as in excel and PNG format in local machine.
2) after successfully converted in excel, png format i will try to send same via email



