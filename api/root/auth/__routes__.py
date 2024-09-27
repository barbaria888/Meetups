from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from root.auth.auth import ForgetPassword, Login, UserRegister
from root.general.currenUser import CurrentUser
from auth.models import User
from app import mongo

# Initialize Blueprint
auth_bp = Blueprint('auth', __name__)

# Initialize User model
user_model = User(mongo)

# Define Auth API Resources
from flask_restful import Api

auth_api = Api(auth_bp)  # Initialize Api with the Blueprint

# Adding resources to the API
auth_api.add_resource(Login, "/api/login")
auth_api.add_resource(UserRegister, "/api/register")
auth_api.add_resource(ForgetPassword, "/api/forget/password")
auth_api.add_resource(CurrentUser, "/api/currentUser")

# Registration Route
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')

    if not full_name or not email or not password:
        return jsonify({'msg': 'Missing data'}), 400

    user_id, error = user_model.register_user(full_name, email, password)
    if error:
        return jsonify({'msg': error}), 400

    return jsonify({'msg': 'User registered successfully', 'user_id': str(user_id)}), 201

# Login Route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = user_model.check_user(email, password)
    if not user:
        return jsonify({'msg': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=str(user['_id']))
    return jsonify({'msg': 'Login successful', 'token': access_token}), 200
