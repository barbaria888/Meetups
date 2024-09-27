from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import logging
import re

logging.basicConfig(level=logging.INFO)

class User:
    def __init__(self, mongo):
        self.users = mongo.db.users

    def is_valid_email(self, email):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(regex, email)

    def register_user(self, full_name, email, password):
        try:
            if not self.is_valid_email(email):
                return None, 'Invalid email format.'
            if self.users.find_one({'email': email}):
                return None, 'User already exists.'

            hashed_password = generate_password_hash(password)
            user_id = self.users.insert_one({
                'full_name': full_name,
                'email': email,
                'password': hashed_password
            }).inserted_id
            logging.info(f'Registered user: {email}')
            return str(user_id), None  # Convert ObjectId to string
        except Exception as e:
            logging.error(f'Error registering user: {e}')
            return None, 'An error occurred while registering.'

    def check_user(self, email, password):
        try:
            user = self.users.find_one({'email': email})
            if user and check_password_hash(user['password'], password):
                return user
            return None
        except Exception as e:
            logging.error(f'Error checking user: {e}')
            return None
