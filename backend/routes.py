from flask import Blueprint, request, jsonify, send_from_directory
from models import User, File
from utils import token_required, generate_verification_token, confirm_verification_token, send_verification_email
import os

auth_bp = Blueprint('auth', __name__)
file_bp = Blueprint('file', __name__)

# Authentication Routes

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    role = data['role']
    
    if User.objects(email=email).first():
        return jsonify({'message': 'User already exists'}), 400
    
    user = User(username=username, email=email, role=role)
    user.set_password(password)
    user.save()

    token = generate_verification_token(email)
    verification_url = f'http://localhost:5000/auth/verify/{token}'
    send_verification_email(email, verification_url)

    return jsonify({'message': 'User registered successfully. Verification email sent!', 'verification_url': verification_url}), 201

@auth_bp.route('/verify/<token>', methods=['GET'])
def verify_email(token):
    email = confirm_verification_token(token)
    if not email:
        return jsonify({'message': 'Invalid or expired token'}), 400

    user = User.objects(email=email).first()
    if user:
        user.is_verified = True
        user.save()
        return jsonify({'message': 'Email verified successfully!'}), 200
    return jsonify({'message': 'User not found'}), 404

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    user = User.objects(email=email).first()
    if user and user.check_password(password):
        return jsonify({'message': 'Login successful', 'user_role': user.role}), 200
    
    return jsonify({'message': 'Invalid email or password'}), 401

# File Routes

@file_bp.route('/upload', methods=['POST'])
@token_required
def upload_file(current_user):
    if current_user.role != 'OpsUser':
        return jsonify({'message': 'Permission denied'}), 403
    
    file = request.files['file']
    if not file:
        return jsonify({'message': 'No file provided'}), 400

    if file.filename.split('.')[-1] not in ['pptx', 'docx', 'xlsx']:
        return jsonify({'message': 'Invalid file type'}), 400
    
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)
    
    new_file = File(filename=file.filename, file_type=file.filename.split('.')[-1], uploaded_by=current_user)
    new_file.save()

    return jsonify({'message': 'File uploaded successfully'}), 201

@file_bp.route('/files', methods=['GET'])
@token_required
def list_files(current_user):
    files = File.objects(uploaded_by=current_user)
    return jsonify(files), 200

@file_bp.route('/download/<file_id>', methods=['GET'])
@token_required
def download_file(current_user, file_id):
    file = File.objects(id=file_id, uploaded_by=current_user).first()
    if not file:
        return jsonify({'message': 'File not found or access denied'}), 404

    download_url = f'http://localhost:5000/files/{file.filename}'
    return jsonify({'download-link': download_url, 'message': 'success'}), 200

@file_bp.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    return send_from_directory('uploads', filename)
