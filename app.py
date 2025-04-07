from flask import Flask, jsonify, render_template, request, redirect
import json
from pymongo import MongoClient  

app = Flask(__name__)

# ✅ MongoDB connection
client = MongoClient("mongodb+srv://Saket:Saket2812@tutedude.hm9ctej.mongodb.net/?retryWrites=true&w=majority&appName=Tutedude")
db = client["mydatabase"]
collection = db["users"]

# ✅ Route for form submission (name/email)
@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form['name']
        email = request.form['email']
        collection.insert_one({'name': name, 'email': email})
        return render_template('success.html')
    except Exception as e:
        return render_template('form.html', error=str(e))

# ✅ Route to show form.html
@app.route('/')
def index():
    return render_template('form.html')  # make sure this file exists in templates/

# ✅ To-Do Form Page (Item Name + Description)
@app.route('/todo')
def todo():
    return render_template('todo.html')  # create a templates/todo.html file

# ✅ To-Do Submission Route
@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    try:
        item_name = request.form['itemName']
        item_desc = request.form['itemDescription']
        collection.insert_one({
            "name": item_name,
            "description": item_desc
        })
        return redirect('/todo')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ API to fetch all data (no _id)
@app.route('/api')
def getdata():
    try:
        data = list(collection.find({}, {'_id': 0}))
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
