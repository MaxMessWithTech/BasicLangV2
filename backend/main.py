from functools import wraps

from flask import Flask, request, jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_socketio import SocketIO, send, emit
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, unset_jwt_cookies, jwt_required, \
	JWTManager, create_refresh_token

from gevent.pywsgi import WSGIServer
import json
import sys
import os
import time
from geventwebsocket.handler import WebSocketHandler

from interpreter import main
from os.path import exists
from interpreter.utils.blcolors import blcolors

# https://flask-socketio.readthedocs.io/en/latest/getting_started.html - Web Sockets
# https://www.geeksforgeeks.org/how-to-connect-reactjs-with-flask-api/ - React

db = SQLAlchemy()

# Initializing flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_TOKEN_LOCATION'] = ["headers", "query_string"]

app.config["JWT_SECRET_KEY"] = "please-remember-to-change-me"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)

db.init_app(app)

socketio = SocketIO(app, cors_allowed_origins='*')

# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'
# login_manager.init_app(app)

# app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app)


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
	email = db.Column(db.String(100), unique=True)
	# password = db.Column(db.String(100))
	password_hash = db.Column(db.String(128))
	name = db.Column(db.String(1000))

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User %r>' % self.email


admin.add_view(ModelView(User, db.session))

# db.create_all(app=app)


"""
@app.after_request
def refresh_expiring_jwts(response):
	try:
		exp_timestamp = get_jwt()["exp"]
		now = datetime.now(timezone.utc)
		target_timestamp = datetime.timestamp(now + timedelta(minutes=10))
		print(f"{target_timestamp} - {exp_timestamp} = {target_timestamp - exp_timestamp} - {target_timestamp > exp_timestamp}")
		if target_timestamp > exp_timestamp:
			access_token = create_access_token(identity=get_jwt_identity())
			data = response.get_json()
			print("Refreshing!")
			if type(data) is dict:
				data["access_token"] = access_token
				response.data = json.dumps(data)
		return response
	except (RuntimeError, KeyError):
		# Case where there is not a valid JWT. Just return the original respone
		return response
"""


@app.route('/token', methods=["POST"])
def create_token():
	email = request.json.get("email", None)
	password = request.json.get("password", None)

	user = User.query.filter_by(email=email).first()

	if not user:
		# user = User(email=email, password=password, name="Max Miller")
		# db.session.add(user)
		# db.session.commit()
		return {"msg": "Wrong email or password"}, 401

	if not user.check_password(password):
		return {"msg": "Wrong email or password"}, 401

	access_token = create_access_token(identity=email)
	refresh_token = create_refresh_token(identity=email)
	response = {"access_token": access_token, "refresh_token": refresh_token}
	return response


@app.route('/join', methods=["POST"])
def handel_join():
	email = request.json.get("email", None)
	password = request.json.get("password", None)
	name = request.json.get("name", None)

	user = User.query.filter_by(email=email).first()

	if not user:
		user = User(email=email, name=name)
		user.set_password(password)
		db.session.add(user)
		db.session.commit()

		access_token = create_access_token(identity=email)
		refresh_token = create_refresh_token(identity=email)
		response = {"access_token": access_token, "refresh_token": refresh_token}
		return response, 201

	return {"msg": "User Already Exists"}, 401


@app.route('/refresh-token', methods=["POST"])
@jwt_required(refresh=True)
def refresh_expiring_jwts():
	identity = get_jwt_identity()
	access_token = create_access_token(identity=identity)
	return jsonify(access_token=access_token)


@app.route('/get-token', methods=["POST"])
@jwt_required(refresh=True)
def get_jwt():
	try:
		access_token = create_access_token(identity=get_jwt_identity())
		response = {"access_token": access_token}
		print(response)
		return response, 202
	except (RuntimeError, KeyError):
		# Case where there is not a valid JWT. Just return the original respone
		return "", 401


@app.route("/logout", methods=["POST"])
def logout():
	response = jsonify({"msg": "logout successful"})
	unset_jwt_cookies(response)
	return response


@app.route('/get-user-files', methods=["POST"])
@jwt_required()
def get_user_files():
	current_user = get_jwt_identity()

	user = User.query.filter_by(email=current_user).first()
	if not user:
		return 'Token Error', 401

	files = list()

	if exists(os.path.realpath(os.path.join(os.path.dirname(__file__), '../storage', str(user.id)))):

		for file in os.listdir(os.path.realpath(os.path.join(os.path.dirname(__file__), '../storage', str(user.id)))):
			if file.endswith(".bsl"):
				files.append({'file': file, 'id': len(files)})
	else:
		os.mkdir(os.path.realpath(os.path.join(os.path.dirname(__file__), '../storage', str(user.id))))

	# emit("setCode", {'data': file.read(), 'fileName': 'script.bsl'})
	return jsonify(files), 200


@app.route('/get-packages', methods=["POST"])
@jwt_required()
def get_available_packages():
	current_user = get_jwt_identity()

	user = User.query.filter_by(email=current_user).first()
	if not user:
		return 'Token Error', 401

	packages = list()

	for (root, dirs, files) in os.walk('./interpreter/components', topdown=True):
		# If there's an __init__.py file we need to find the objects in that python package
		if "__init__.py" in files:
			# This imports the __init__.py file, and sets its reference to the module var
			for package in dirs:
				if package != "__pycache__":
					packages.append({'_package': package, 'id': len(packages)})

	return jsonify(packages), 200


@app.route('/create-file', methods=["POST"])
@jwt_required()
def create_file():
	current_user = get_jwt_identity()

	user = User.query.filter_by(email=current_user).first()

	fileName = request.json.get("fileName", None)

	if not user:
		return 'Token Error', 401
	if exists(os.path.realpath(os.path.join(os.path.dirname(__file__), '../storage', str(user.id), fileName))):
		return 'File Already Exists', 400

	if exists(os.path.realpath(os.path.join(os.path.dirname(__file__), '../storage', str(user.id)))):
		if exists(os.path.realpath(os.path.join(os.path.dirname(__file__), '../storage', str(user.id), fileName))):
			file = open(
				os.path.realpath(os.path.join(os.path.dirname(__file__), '../storage', str(user.id), fileName)), "r")
		else:
			file = open(
				os.path.realpath(os.path.join(os.path.dirname(__file__), '../storage', str(user.id), fileName)), "w+")
	else:
		os.mkdir(os.path.realpath(os.path.join(os.path.dirname(__file__), '../storage', str(user.id))))
		file = open(os.path.realpath(os.path.join(os.path.dirname(__file__), '../storage', str(user.id), fileName)), "w+")

	# emit("setCode", {'data': file.read(), 'fileName': 'script.bsl'})
	return "Created", 201


@socketio.on('message')
@jwt_required()
def handle_message(message):
	print('Data', message)


@socketio.on('load')
@jwt_required()
def handle_load(fileName):
	current_user = get_jwt_identity()

	user = User.query.filter_by(email=current_user).first()
	if not user:
		return 'Token Error', 401
	if exists(os.path.realpath(os.path.join(os.path.dirname(__file__), '../storage', str(user.id)))):
		if exists(os.path.realpath(os.path.join(os.path.dirname(__file__), '../storage', str(user.id), fileName))):
			file = open(
				os.path.realpath(os.path.join(os.path.dirname(__file__), '../storage', str(user.id), fileName)), "r")
		else:
			file = open(
				os.path.realpath(os.path.join(os.path.dirname(__file__), '../storage', str(user.id), fileName)), "w+")
	else:
		os.mkdir(os.path.realpath(os.path.join(os.path.dirname(__file__), '../storage', str(user.id))))
		file = open(os.path.realpath(os.path.join(os.path.dirname(__file__), '../storage', str(user.id), fileName)), "w+")

	emit("setCode", {'data': file.read(), 'fileName': fileName})


# file.close()


@socketio.on('save')
@jwt_required()
def handle_save(code, fileName):
	current_user = get_jwt_identity()

	user = User.query.filter_by(email=current_user).first()
	if not user:
		return 'Token Error', 401
	if exists(os.path.realpath(os.path.join(os.path.dirname(__file__), '../storage', str(user.id)))):
		file = open(os.path.realpath(os.path.join(os.path.dirname(__file__), '../storage', str(user.id), fileName)), "w")
		file.write(code)
	else:
		os.mkdir(os.path.realpath(os.path.join(os.path.dirname(__file__), '../storage', str(user.id))))
		file = open(os.path.realpath(os.path.join(os.path.dirname(__file__), '../storage', str(user.id), fileName)), "w")
		file.write(code)

	# file.close()


def execution_callback(cmd, data, **kwargs):
	if cmd == "error" or cmd == "debug" or cmd == "log":
		# print(f"{blcolors.YELLOW}[{cmd}]: {data}{blcolors.CLEAR}")
		emit('log', data)
	elif cmd == "draw":
		emit("draw", json.dumps(data))
		# Complies all the values into one value
		for x in range(len(data['cords'])):
			data['cords'][x] = (data['cords'][x]['x'], data['cords'][x]['y'])

		# Shortens for printing
		if len(data['cords']) > 3:
			data['cords'] = data['cords'][0:3]
			print(f"{blcolors.YELLOW}[{cmd}]: {data} {blcolors.MAGENTA}SHORTENED{blcolors.CLEAR}")
		else:
			print(f"{blcolors.YELLOW}[{cmd}]: {data}{blcolors.CLEAR}")
	else:
		print(f"{blcolors.YELLOW}{blcolors.BOLD}[Callback]{blcolors.CLEAR}" +
		      f"{blcolors.YELLOW} [{cmd}]: {repr(data)}{blcolors.CLEAR}")


@socketio.on('sendCode')
@jwt_required()
def handle_send_code(code, fileName):
	print(f"Send Code! {code}")

	handle_save(code, fileName)

	current_user = get_jwt_identity()

	user = User.query.filter_by(email=current_user).first()
	if not user:
		return 'Token Error', 401

	filePath = os.path.realpath(os.path.join(os.path.dirname(__file__), '../storage', str(user.id), fileName))

	file_exists = exists(filePath)
	if file_exists:
		file = open(filePath, "r")
		# print(file.readlines())
		# file.write(code)
		main.run(file, sendCommandCallback=execution_callback)
	else:
		print(f"{blcolors.RED}Invalid filename: {repr(filePath)}{blcolors.CLEAR}")


@socketio.on('connect')
@jwt_required()
def handle_connect():
	try:
		current_user = get_jwt_identity()

		user = User.query.filter_by(email=current_user).first()
		if not user:
			return 'Token Error', 401

		print(f'New Connection (Auth: {current_user})')
		emit('my response', {'data': 'Connected'})
	except:
		return 'Token Error', 401


@socketio.on('disconnect')
def test_disconnect():
	print('Client disconnected')


# Running app
if __name__ == '__main__':
	http_server = WSGIServer(('', 5000), app)
	http_server.serve_forever()
# app.run(debug=True)
# socketio.run(app, debug=True)
