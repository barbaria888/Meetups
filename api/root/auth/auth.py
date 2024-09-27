from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from pymongo import MongoClient
from marshmallow import Schema, fields, ValidationError

# Import your configurations
from api.root.config import MONGO_URI, MONGO_DATABASE
from root.general.commonUtilis import (
    bcryptPasswordHash,
    cleanupEmail,
    maskEmail,
    mdbObjectIdToStr,
    verifyPassword,
)
from root.general.authUtils import validate_auth
from root.static import G_ACCESS_EXPIRES


def connect_mongodb(uri, db_name):
    client = MongoClient(uri)
    db = client[db_name]
    return db

mdb = connect_mongodb(MONGO_URI, MONGO_DATABASE)

# Marshmallow Schema for validation
class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class Login(Resource):
    def post(self):
        data = request.get_json()
        try:
            validated_data = LoginSchema().load(data)
        except ValidationError as err:
            return {"status": 0, "cls": "error", "msg": err.messages}, 400

        email = validated_data['email']
        password = validated_data['password']

        user = db.users.find_one({"email": email})
        if not user or not check_password_hash(user["password"], password):
            return {"status": 0, "cls": "error", "msg": "Invalid email or password."}, 401

        access_token = create_access_token(identity=str(user["_id"]))
        return {"status": 1, "cls": "success", "msg": "Login successful", "token": access_token}, 200
def login(data):
    email = cleanupEmail(data.get("email"))

    # Additional filter conditions
    filter_condition = {"email": email, "status": {"$nin": ["deleted", "removed", "suspended"]}}
    
    userDoc = mdb.users.find_one(filter_condition)

    if not (userDoc and "_id" in userDoc):
        return {
            "status": 0,
            "cls": "error",
            "msg": "Invalid email id and password. Please try again",
        }

    if userDoc.get("status") == "pending":
        return {
            "status": 0,
            "cls": "error",
            "msg": "Your Request is still pending. Contact admin for more info.",
            "payload": {
                "redirect": "/adminApproval",
                "userMeta": userDoc,
            },
        }

    # Check password
    if not verifyPassword(userDoc["password"], data.get("password")):
        return {
            "status": 0,
            "cls": "error",
            "msg": "Invalid email id and password. Please try again",
        }

    # Create access token and prepare payload
    uid = mdbObjectIdToStr(userDoc["_id"])
    access_token = create_access_token(identity=uid, expires_delta=G_ACCESS_EXPIRES)

    payload = {
        "accessToken": access_token,
        "uid": uid,
        "redirectUrl": "/dashboard",
    }

    return {
        "status": 1,
        "cls": "success",
        "msg": "Login successful. Redirecting...",
        "payload": payload,
    }

# Schema for user registration validation
class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    avatarUrl = fields.Str(missing="/avatar.svg")

class UserRegister(Resource):
    @validate_auth(optional=True)
    def post(self, suid, suser):
        input_data = request.get_json()

        # Marshmallow validation
        try:
            validated_data = RegisterSchema().load(input_data)
        except ValidationError as err:
            return {"status": 0, "cls": "error", "msg": err.messages}, 400

        email = validated_data["email"]
        
        currentUser = mdb.users.find_one({"email": email})

        if currentUser and "_id" in currentUser:
            maskedEmail = maskEmail(email)
            return {
                "status": 0,
                "cls": "error",
                "msg": f"Email ID ({maskedEmail}) already exists",
                "payload": {},
            }

        # Clean up and hash the password
        newPassword = bcryptPasswordHash(validated_data["password"])
        avatarUrl = validated_data["avatarUrl"]

        newUser = {
            "email": email,
            "password": newPassword,
            "avatarUrl": avatarUrl,
            "status": "active",
        }

        mdb.users.insert_one(newUser)

        payload = {
            "ruid": newUser["_id"],
            "redirect": "/login",
        }

        return {
            "status": 1,
            "cls": "success",
            "msg": "Congratulations! You have successfully registered. Please login to continue.",
            "payload": payload,
        }

class UserLogout(Resource):
    @validate_auth(optional=True)
    def post(self, suid, suser):
        content = request.get_json(silent=True)

    

        return {
            "status": 1,
            "cls": "success",
            "msg": "Logged out successfully!",
        }
    
class ForgetPassword(Resource):
    @validate_auth(optional=True)
    def post(self, suid, suser):
        # Get the input JSON data from the request
        input_data = request.get_json()

        # Check if both email and newPassword fields are present in the input
        if not input_data or not input_data.get("email") or not input_data.get("newPassword"):
            return {"status": 0, "cls": "error", "msg": "Email and new password are required."}, 400

        # Clean up the email address (remove extra spaces, convert to lowercase)
        email = cleanupEmail(input_data["email"])
        
         # Find the user in MongoDB by email
        user = mdb.users.find_one({"email": email})
        
         # Check if the user exists
        if not user:
             return {
                 "status": 0,
                 "cls": "error",
                 "msg": f"User with email {email} not found.",
                 'payload': {},
             }, 404

         # Hash the new password
        hashedPassword = bcryptPasswordHash(input_data["newPassword"])

         # Update the user document with the new hashed password and set 'defaultPassword' to False
        update_result = mdb.users.update_one(
             {"_id": user["_id"]},
             {"$set": {"password": hashedPassword, 'defaultPassword': False}}
         )

         # Check if the update was successful
        if update_result.modified_count == 0:
             return {
                 'status': 0,
                 'cls': 'error',
                 'msg': 'Failed to reset password. Please try again.',
                 'payload': {}
             }, 500
 
         # Return success response
        return {
             'status': 1,
             'cls': 'success',
             'msg': 'Password reset successfully.',
             'payload': {}
         }, 200