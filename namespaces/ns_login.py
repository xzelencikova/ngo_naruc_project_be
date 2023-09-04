from flask_restx import Namespace, Resource
from namespaces.ns_naruc import api

from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client['your_db_name']
users_collection = db['users']

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    user = users_collection.find_one({'email': email})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({
            'name': user['name'],
            'surname': user['surname'],
            'email': user['email'],
            'role': user['role']
        }), 200
    else:
        return 'Not Found', 404

@app.route('/sign_in', methods=['POST'])
def sign_in():
    data = request.json
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    user_data = {
        'name': data['name'],
        'surname': data['surname'],
        'email': data['email'],
        'role': data['role'],
        'password': hashed_password
    }

    users_collection.insert_one(user_data)
    return 'User created', 200

@app.route('/users', methods=['GET'])
def get_users():
    users = list(users_collection.find({}, {'_id': 0, 'password': 0}))
    return jsonify(users), 200

@app.route('/role/<user_id>', methods=['PUT'])
def update_role(user_id):
    new_role = request.json['role']
    users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'role': new_role}})
    return '', 200

@app.route('/user/<user_id>', methods=['PUT'])
def update_user_info(user_id):
    # Implement updating user info based on request
    return '', 200

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    users_collection.delete_one({'_id': ObjectId(user_id)})
    return '', 200

if __name__ == '__main__':
    app.run(debug=True)

