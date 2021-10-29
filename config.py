from flask import *
import mysql.connector


app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="data"
)

# mydb = mysql.connector.connect(
#     host="us-cdbr-east-04.cleardb.com",
#     user="b0da91e06ee504",
#     password="6b0f2bdb",
#     database="heroku_b521556c7f4725f"
# )
cursor = mydb.cursor()



if __name__ =='__main__':
    app.run(debug=True)