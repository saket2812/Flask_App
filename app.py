from flask import Flask, jsonify, render_template, request, redirect
import json
from pymongo import MongoClient  

app = Flask(__name__)


client = MongoClient("mongodb+srv://Saket:Saket2812@tutedude.hm9ctej.mongodb.net/?retryWrites=true&w=majority&appName=Tutedude")
db = client["mydatabase"]
collection = db["users"]


@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form['name']
        email = request.form['email']
        collection.insert_one({'name': name, 'email': email})
        return render_template('success.html')
    except Exception as e:
        return render_template('form.html', error=str(e))


@app.route('/')
def index():
    return render_template('form.html')  # make sure this file exists in templates/


@app.route('/todo')
def todo_page():
    success = request.args.get('success')
    return render_template('Todo.html', success=success)



@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    try:
        item_name = request.form['itemName']
        item_desc = request.form['itemDescription']

        collection.insert_one({
            "name": item_name,
            "description": item_desc
        })

        # Redirect with success flag
        return redirect('/todo?success=1')
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@app.route('/api')
def getdata():
    try:
        data = list(collection.find({}, {'_id': 0}))
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
