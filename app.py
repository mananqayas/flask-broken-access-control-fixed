from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = 'mysecretkey'
jwt = JWTManager(app)


CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
user = {"admin": "password123"}
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username in user and user[username] == password:
        access_token = create_access_token(identity=str(username), fresh=True)
        return jsonify(access_token=access_token)
    return jsonify({"message": "Invalid credentials", "status": 401}), 401
@app.route('/admin', methods=["GET"])
@jwt_required()
def admin():
    current_user  = get_jwt_identity()
    return jsonify(logged_in_as=current_user, message="This is protected content"), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)