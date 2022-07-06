from functools import wraps

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send, emit
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager

from gevent.pywsgi import WSGIServer
import json
import sys
import os
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
app.config['JWT_TOKEN_LOCATION'] = ['query_string']

app.config["JWT_SECRET_KEY"] = "please-remember-to-change-me"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

db.init_app(app)

socketio = SocketIO(app, cors_allowed_origins='*')

login_manager = LoginManager()
# login_manager.login_view = 'auth.login'
login_manager.init_app(app)


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(100))
	name = db.Column(db.String(1000))

	def check_password(self, password):
		if password == self.password:
			return True
		return False

	def __repr__(self):
		return '<User %r>' % self.email


# db.create_all(app=app)


@app.after_request
def refresh_expiring_jwts(response):
	try:
		exp_timestamp = get_jwt()["exp"]
		now = datetime.now(timezone.utc)
		target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
		if target_timestamp > exp_timestamp:
			access_token = create_access_token(identity=get_jwt_identity())
			data = response.get_json()
			if type(data) is dict:
				data["access_token"] = access_token
				response.data = json.dumps(data)
		return response
	except (RuntimeError, KeyError):
		# Case where there is not a valid JWT. Just return the original respone
		return response


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
	response = {"access_token": access_token}
	return response


@app.route('/join', methods=["POST"])
def create_token():
	email = request.json.get("email", None)
	password = request.json.get("password", None)
	name = request.json.get("name", None)

	user = User.query.filter_by(email=email).first()

	if not user:
		user = User(email=email, password=password, name=name)
		db.session.add(user)
		db.session.commit()

		access_token = create_access_token(identity=email)
		response = {"access_token": access_token}
		return response, 201

	return {"msg": "User Already Exists"}, 401


@app.route('/profile')
@jwt_required()
def my_profile():
	response_body = {
		"name": "Nagato",
		"about": "Hello! I'm a full stack developer that loves python and javascript"
	}

	return response_body


@app.route("/logout", methods=["POST"])
def logout():
	response = jsonify({"msg": "logout successful"})
	unset_jwt_cookies(response)
	return response


@socketio.on('message')
def handle_message(message):
	print('Data', message)


@socketio.on('load')
def handle_load():
	print("Load!")

	file = open(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'script.bsl')))

	emit("setCode", file.read())


@socketio.on('save')
def handle_save(code):
	file = open(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'script.bsl')), "w")
	file.write(code)


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
def handle_send_code(code):
	print("Send Code!")

	handle_save(code)

	fileName = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'script.bsl'))

	file_exists = exists(fileName)
	if file_exists:
		file = open(fileName, "r")
		# print(file.readlines())
		# file.write(code)
		main.run(file, sendCommandCallback=execution_callback)
	else:
		print(f"{blcolors.RED}Invalid filename: {repr(fileName)}{blcolors.CLEAR}")


@socketio.on('connect')
@jwt_required()
def test_connect():
	try:
		current_user = get_jwt_identity()

		user = User.query.filter_by(email=current_user).first()
		if not user:
			raise ConnectionRefusedError('unauthorized!')

		print(f'New Connection (Auth: {current_user})')
		emit('my response', {'data': 'Connected'})
	except:
		raise ConnectionRefusedError('unauthorized!')


@socketio.on('disconnect')
def test_disconnect():
	print('Client disconnected')


# Running app
if __name__ == '__main__':
	http_server = WSGIServer(('', 5000), app)
	http_server.serve_forever()
# app.run(debug=True)
# socketio.run(app, debug=True)
