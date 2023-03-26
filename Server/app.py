from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
import jwt
import datetime


app = Flask(__name__)
CORS(app,resources={r'/*': {'origins': '*'}})

app.config['MONGO_URI'] = 'mongodb://localhost:27017/ImageApp'
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'thisisthesecretkey'

def create_token(user_id):
    payload = {'user_id': str(user_id), 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}
    token = jwt.encode(payload, app.config['SECRET_KEY'])
    return token

@app.route('/login', methods=['POST'])
def login():
    print(request)
    user = mongo.db.users.find_one({'email': request.json['email']})
    if user and bcrypt.check_password_hash(user['password'], request.json['password']):
        token = create_token(user['_id'])
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/register', methods=['POST'])
def register():
    user = mongo.db.users.find_one({'email': request.json['email']})
    if user:
        return jsonify({'message': 'User already exists'}), 400
    else:
        password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
        user_id = mongo.db.users.insert_one({'email': request.json['email'], 'password': password})
        token = create_token(user_id)
        return jsonify({'token': token}), 201

@app.route("/api/upload-image", methods=["POST"])
def upload_image():
    image = request.files.get('image')
    # filename = secure_filename(image.filename)
    # image.save(os.path.join("./uploads", filename))
    print(image)
    return jsonify({'message': 'mEUSNId1Hfc'})

@app.route('/')
def index():
    return jsonify({'message': 'Success'})

if __name__ == '__main__':
    app.run(debug=True,host='0000.0000.0808',port=3000)