from flask import Flask, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Student'
app.config['MYSQL_DB'] = 'library_db'

mysql = MySQL(app)

@app.route('/')
def home():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        cur.close()
        return "Flask + MySQL working 🚀"
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)
