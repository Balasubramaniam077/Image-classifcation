from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
import jwt
import datetime
import io
import cv2
import string
import numpy as np
import torch
import torch.nn as nn

from flask import Flask, jsonify, render_template, request, redirect
from torch.autograd import Variable
from torchvision import models, transforms
from PIL import Image

app = Flask(_name_)
CORS(app,resources={r'/': {'origins': ''}})

app.config['MONGO_URI'] = 'mongodb+srv://vbala2k21:image classification@cluster0.anq8cdc.mongodb.net/test'
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
MODEL_PATH = "./model/dense_net.pt"
device = torch.device("cpu")
class_names = [
    "Bean_Angular_Leaf_Spot",
    "Bean_Heathly",
    "Bean_Rust",
    "Cotton_Disease",
    "Cotton_Healthy",
    "Cucumber_Disease",
    "Cucumber_Healthy",
    "Guava_Disease",
    "Guava_Healthy",
    "Lemon_Diseased",
    "Lemon_Healthy",
    "Mango_Disease",
    "Mango_Healthy",
    "Pomegranate_Diseased",
    "Pomegranate_Healthy",
    "Potato_Early_Blight",
    "Potato_Healthy",
    "Potato_Late_Blight",
    "Tea_Disease",
    "Tea_Healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___healthy",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
]


# Defining Model Architecture
def CNN_model(pretrained):
    inf_model = models.densenet121(pretrained=pretrained)
    inf_model.classifier.in_features = len(class_names)
    inf_model.to(torch.device("cpu"))
    return inf_model


inf_model = CNN_model(pretrained=False)

# Loading the Model Trained Weights
inf_model.to(torch.device("cpu"))
inf_model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
inf_model.eval()
print("Inference model Loaded on CPU")

# Image Transform
def transform_image(image_bytes):
    test_transforms = transforms.Compose(
        [
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
        ]
    )
    image = Image.open(io.BytesIO(image_bytes))
    image = np.array(image)
    if image.shape[-1] == 4:
        image_cv = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    if image.shape[-1] == 3:
        image_cv = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    if len(image.shape) == 2:
        image_cv = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    return test_transforms(image_cv).unsqueeze(0)


def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = inf_model.forward(tensor)
    _, prediction = torch.max(outputs, 1)
    print(prediction)
    return class_names[prediction]

@app.route("/api/upload-image", methods=["POST"])
def upload_image():
    image = request.files.get('image')
    if not image:
            return
    img_bytes = image.read()
    prediction_name = get_prediction(img_bytes)
    return jsonify({'message':prediction_name.lower()})
    # filename = secure_filename(image.filename)
    # image.save(os.path.join("./uploads", filename))

@app.route('/')
def index():
    return jsonify({'message': 'Success'})

if _name_ == '_main_':
    app.run(debug=True,host='0000.0000.0808',port=3000)
