from flask import *
import mysql.connector



app = Flask(__name__)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="data"
)


if __name__ =='__main__':
    app.run(debug=True)