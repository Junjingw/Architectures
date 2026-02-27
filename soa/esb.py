# esb.py
from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Simulated service registry
services = {
    'books': 'http://books:5001/books',
    'loans': 'http://loans:5002/loans',
    'notifications': 'http://notifications:5003/notifications'
}

# Message transformation and routing
@app.route('/services/<service>/<path:subpath>', methods=['GET', 'POST', 'PUT'])
def route_request(service, subpath):
    if service not in services:
        return jsonify({"error": "Service not found"}), 404
    
    # Message transformation
    headers = {'Content-Type': 'application/json'}
    target_url = f"{services[service]}/{subpath}"
    
    try:
        if request.method == 'GET':
            response = requests.get(target_url)
        elif request.method == 'POST':
            # Transform message if needed
            data = request.json
            response = requests.post(target_url, json=data, headers=headers)
        elif request.method == 'PUT':
            data = request.json
            response = requests.put(target_url, json=data, headers=headers)
            
        return response.json(), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({"error": "Service unavailable"}), 503

# Service composition example: Borrow book process
@app.route('/processes/borrow', methods=['POST'])
def borrow_process():
    data = request.json
    book_id = data.get('book_id')
    user_id = data.get('user_id')
    
    try:
        # Check book availability
        book_response = requests.get(f"{services['books']}/{book_id}")
        if not book_response.ok:
            return jsonify({"error": "Book not found"}), 404
            
        book = book_response.json()
        if book.get('borrowed'):
            return jsonify({"error": "Book already borrowed"}), 400
            
        # Create loan
        loan_data = {"book_id": book_id, "user_id": user_id}
        loan_response = requests.post(services['loans'], json=loan_data)
        if not loan_response.ok:
            return jsonify({"error": "Failed to create loan"}), 500
            
        # Send notification
        notif_data = {
            "user_id": user_id,
            "message": f"Book '{book.get('title')}' has been borrowed successfully"
        }
        requests.post(services['notifications'], json=notif_data)
        
        return loan_response.json(), 200
        
    except requests.exceptions.RequestException:
        return jsonify({"error": "Service unavailable"}), 503

if __name__ == '__main__':
    app.run(port=5000,host='0.0.0.0')