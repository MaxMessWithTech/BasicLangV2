from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import datetime
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

x = datetime.datetime.now()

# Initializing flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')


@socketio.on('message')
def handle_message(message):
	print('Data', message)


@socketio.on('load')
def handle_load():
	print("Load!")

	file = open(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'script.bsl')))

	emit("setCode", file.read())


# emit("log", json.dumps(["WEEEE"]))


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
def test_connect(auth):
	print(f'New Connection (Auth: {auth})')
	emit('my response', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
	print('Client disconnected')


# Running app
if __name__ == '__main__':
	http_server = WSGIServer(('', 5000), app)
	http_server.serve_forever()
# app.run(debug=True)
# socketio.run(app, debug=True)
