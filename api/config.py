import datetime
import json
import os
from bson.objectid import ObjectId
import bson

from settings import (
    G_API_URL,
    G_JWT_ACCESS_SECRET_KEY,
    LOCAL_MONGO_URI,
    LOCAL_MONGO_DATABASE,
    JWT_SECRET_KEY,
    MONGO_URI,
    MONGO_DATABASE,
    ROOT_DIR,
    G_TEMP_PATH
)
class CustomFlaskResponseEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return str(obj)
        elif isinstance(obj, datetime.date):
            return str(obj)
        elif isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, bson.ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

class Config:
    JWT_SECRET_KEY = G_JWT_ACCESS_SECRET_KEY
    
    @staticmethod
    def get_token_expiry():
        from root.static import G_ACCESS_EXPIRES, G_REFRESH_EXPIRES
        return G_ACCESS_EXPIRES, G_REFRESH_EXPIRES

    JWT_ACCESS_TOKEN_EXPIRES, JWT_REFRESH_TOKEN_EXPIRES = get_token_expiry()

    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
    PROPAGATE_EXCEPTIONS = True
    TRAP_HTTP_EXCEPTIONS = True
    MAX_CONTENT_LENGTH = 16 * 1000 * 1000
    RESTFUL_JSON = {
        "cls": CustomFlaskResponseEncoder,
    }
