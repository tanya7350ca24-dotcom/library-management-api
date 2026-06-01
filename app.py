from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)


DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "Student",  
    "database": "library_db"
}


@app.route('/')
def home():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("SELECT 1")
        result = cursor.fetchone()  

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Flask + MySQL working 🚀",
            "result": result
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })



if __name__ == "__main__":
    app.run(debug=True)
