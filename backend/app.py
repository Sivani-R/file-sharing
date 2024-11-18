from flask import Flask
from flask_cors import CORS
from routes import auth_bp, file_bp
from config import Config
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db = MongoEngine(app)

app.register_blueprint(auth_bp)
app.register_blueprint(file_bp)

if __name__ == '__main__':
    app.run(debug=True)
