import os
G_API_URL = "http://localhost:5000"

# ℹ️ It is recommended to use environment variables for the secret key
G_JWT_ACCESS_SECRET_KEY = "ABCDEFGHIJKLMN"
LOCAL_MONGO_URI = "mongodb://localhost:27017"
LOCAL_MONGO_DATABASE = "userdatabase"
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'ABCDEFGHIJKLMN')
### Local DB
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
MONGO_DATABASE = LOCAL_MONGO_DATABASE

# --------------------- Local Folder Settings----------------------------
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
G_TEMP_PATH = os.path.abspath(os.path.join(ROOT_DIR, "..", "temp"))
