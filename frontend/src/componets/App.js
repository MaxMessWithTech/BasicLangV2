import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';

import './App.css';
import Editor from './Editor'

function App() {
	const [socket, setSocket] = useState(null);

	useEffect(() => {

		const socket = io.connect("http://localhost:5000", {
			// autoConnect: false,
			reconnection: true,
			// transports: ['websocket']
		});

		// socket.emit("message", {'data': 'test!'})

		setSocket(socket);

		// exports.socket = socket;
	}, [setSocket]);

	return (
		<div className="d-flex align-items-center justify-content-center fullSize">
			{ socket ? (
				<Editor socket={socket}/>
			) : (
				<div>Not Connected</div>
			)}
		</div>
	);
}

export default App;