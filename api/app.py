from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from config import Config
from root.auth import auth_bp  

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

mongo = PyMongo(app)
jwt = JWTManager(app)


app.register_blueprint(auth_bp, url_prefix='/api/auth')

if __name__ == '__main__':
    app.run(debug=True)
