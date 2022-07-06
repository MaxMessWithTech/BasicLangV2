import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'

import './App.css';
import Editor from './Editor'
import useToken from './useToken';
import Nav from "./nav";
import Login from "./login"

function App() {
	const [socket, setSocket] = useState(null);
	const { token, removeToken, setToken } = useToken();

	useEffect(() => {

		const socket = io.connect("http://localhost:5000", {
			// autoConnect: false,
			reconnection: true,
			query: { 'jwt': token }
			// transports: ['websocket']
		});

		// socket.emit("message", {'data': 'test!'})

		setSocket(socket);

		// exports.socket = socket;
	}, [setSocket]);

	return (
		<Router>
			<Nav loggedIn={!(!token && token !== "" && token !== undefined)} removeToken={removeToken}/>
			<Routes>
				<Route path="/login" exact element={<Login setToken={setToken}/>} />

		        <Route path="/" element={
					!token && token!=="" &&token!== undefined
						? <Navigate to="/login" />
						: <div className="d-flex align-items-center justify-content-center flex-column fullSize">
							{ socket ? (
								<Editor socket={socket} token={token}/>
							) : (
								<div>Not Connected</div>
							)}
						</div>
		        } />
			</Routes>
		</Router>
	);
}

export default App;