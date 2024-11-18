from flask_mongoengine import MongoEngine
from flask.json import json_encoder as JSONEncoder

from werkzeug.security import generate_password_hash, check_password_hash

db = MongoEngine()

class User(db.Document):
    username = db.StringField(required=True, unique=True)
    email = db.StringField(required=True, unique=True)
    password_hash = db.StringField(required=True)
    is_verified = db.BooleanField(default=False)
    role = db.StringField(required=True) 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class File(db.Document):
    filename = db.StringField(required=True)
    file_type = db.StringField(required=True)
    uploaded_by = db.ReferenceField(User)
