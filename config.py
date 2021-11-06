from flask import *
# import mysql.connector
import pymysql

app = Flask(__name__)

# mydb = pymysql.connect(
#     host="localhost",
#     user="root",
#     password="root",
#     database="data"
# )
#
mydb = pymysql.connect(
        host="us-cdbr-east-04.cleardb.com",
        user="b0da91e06ee504",
        password="6b0f2bdb",
        database="heroku_b521556c7f4725f"
    )

a = 0
while a == 0:
    mydb.connect()
    cursor = mydb.cursor()
    a = 1

if __name__ =='__main__':
    app.run(debug=True)