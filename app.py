from flask import Flask, jsonify, render_template, request
import json
from pymongo import MongoClient  

app = Flask(__name__)

# ✅ Correct the MongoClient import and usage
client = MongoClient("mongodb+srv://Saket:Saket2812@tutedude.hm9ctej.mongodb.net/?retryWrites=true&w=majority&appName=Tutedude")
db = client["mydatabase"]
collection = db["users"]


@app.route('/todo')
def todo():
    return render_template('Todo.html')

@app.route('/')
def index():
    return render_template('form.html')  # 🔄 Make sure the filename is all lowercase (form.html)

@app.route('/api')
def getdata():
    try:
        # Get all documents and exclude MongoDB's default _id field
        data = list(collection.find({}, {'_id': 0}))
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form['name']
        email = request.form['email']
        collection.insert_one({'name': name, 'email': email})
        return render_template('success.html')
    except Exception as e:
        return render_template('form.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
