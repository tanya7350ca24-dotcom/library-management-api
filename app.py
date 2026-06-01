from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "Student",
    "database": "library_db"
}

@app.route('/')
def home():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        return "Flask + MySQL CONNECTED 🚀"
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)
