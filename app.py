@app.route('/')
def home():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        cur.close()
        return "Flask → MySQL connection SUCCESS 🚀"
    except Exception as e:
        return f"Connection failed: {str(e)}"
