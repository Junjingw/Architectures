# books_service.py
from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {"id": 1, "title": "Don Quijote", "borrowed": False},
    {"id": 2, "title": "Cien años de soledad", "borrowed": False}
]

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b['id'] == book_id), None)
    if book:
        return jsonify(book)
    return '', 404

if __name__ == '__main__':
    app.run(port=5001,host='0.0.0.0')