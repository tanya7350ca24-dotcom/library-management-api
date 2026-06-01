from flask import Flask, request, jsonify
import mysql.connector
from config import DB_CONFIG

app = Flask(__name__)

# ---------------- DATABASE CONNECTION ----------------
def get_db():
    return mysql.connector.connect(**DB_CONFIG)

# ---------------- HOME ----------------
@app.route('/')
def home():
    return jsonify({
        "message": "Library Management API is running",
        "version": "1.0",
        "endpoints": {
            "GET    /books":      "Get all books",
            "GET    /books/<id>": "Get one book",
            "POST   /books":      "Add a book",
            "PUT    /books/<id>": "Update a book",
            "DELETE /books/<id>": "Delete a book"
        }
    })

# ---------------- POST: ADD BOOK ----------------
@app.route('/books', methods=['POST'])
def add_book():
    try:
        data = request.json
        if not data or not all(k in data for k in ('title', 'author', 'quantity')):
            return jsonify({"error": "title, author and quantity are required"}), 400
        db = get_db()
        cursor = db.cursor()
        sql = "INSERT INTO books (title, author, quantity) VALUES (%s, %s, %s)"
        cursor.execute(sql, (data['title'], data['author'], data['quantity']))
        db.commit()
        new_id = cursor.lastrowid
        cursor.close()
        db.close()
        return jsonify({"message": "Book added successfully", "id": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- GET: ALL BOOKS ----------------
@app.route('/books', methods=['GET'])
def get_books():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        cursor.close()
        db.close()
        result = []
        for book in books:
            result.append({
                "id":       book[0],
                "title":    book[1],
                "author":   book[2],
                "quantity": book[3]
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- GET: SINGLE BOOK ----------------
@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM books WHERE id=%s", (id,))
        book = cursor.fetchone()
        cursor.close()
        db.close()
        if book:
            return jsonify({
                "id":       book[0],
                "title":    book[1],
                "author":   book[2],
                "quantity": book[3]
            }), 200
        return jsonify({"message": "Book not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- PUT: UPDATE BOOK ----------------
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    try:
        data = request.json
        if not data or not all(k in data for k in ('title', 'author', 'quantity')):
            return jsonify({"error": "title, author and quantity are required"}), 400
        db = get_db()
        cursor = db.cursor()
        sql = "UPDATE books SET title=%s, author=%s, quantity=%s WHERE id=%s"
        cursor.execute(sql, (data['title'], data['author'], data['quantity'], id))
        db.commit()
        affected = cursor.rowcount
        cursor.close()
        db.close()
        if affected == 0:
            return jsonify({"message": "Book not found"}), 404
        return jsonify({"message": "Book updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- DELETE: DELETE BOOK ----------------
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM books WHERE id=%s", (id,))
        db.commit()
        affected = cursor.rowcount
        cursor.close()
        db.close()
        if affected == 0:
            return jsonify({"message": "Book not found"}), 404
        return jsonify({"message": "Book deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)