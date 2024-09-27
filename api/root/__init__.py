from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from root.config import Config

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    app.debug = True

    # Initialize CORS
    CORS(app, resources={r"/*": {"origins": "*"}})  # Specify origins if possible

    # Initialize JWT
    jwt = JWTManager(app)

    # Initialize API
    api = Api(app)

    # Register resources and blueprints
    from root.home import Home
    from root.auth import auth_bp
    from root.dashboard import dashboard_bp
    api.add_resource(Home, "/", endpoint="Home")
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp, url_prefix="/api")
    return app
    
if __name__ == "__main__":
    app = create_app()
    app.run()   
