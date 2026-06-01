@app.route('/')
def home():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        cur.close()
        return "SUCCESS: Flask connected to MySQL 🚀"
    except Exception as e:
        return f"FAILED: {str(e)}"
