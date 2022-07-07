import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'

import './App.css';
import Editor from './Editor'
import useToken from './useToken';
import Nav from "./nav";
import Login from "./login"
import Join from "./join"
import axios from "axios";

function App() {
	const [socket, setSocket] = useState(null);
	const { token, refToken, setRefToken, removeToken, setToken } = useToken();

	useEffect(() => {
		if (token == null) {
			// console.log("Token: " + token);
			//console.log("Ref Token: " + refToken);
			if (refToken != null) {
				axios({
					method: "POST",
					url: "/get-token",
					headers: {
						Authorization: `Bearer ${refToken}`,
					}
				}).then((response) => {
					// console.log(response)
					if (response.status === 202) {
						setToken(response.data.access_token)
						// console.log("recived Token: " + response.data.access_token)
					}

				}).catch((error) => {
					if (error.response) {
						// console.log(error.response)
						// console.log(error.response.status)
						// console.log(error.response.headers)
						removeToken();
					}
				})
			} else { setToken(""); }
		}
	}, []);

	useEffect(() => {
		// console.log("TEST 2 TEST")
		// console.log("Token: " + token);
		if (token != null && token !== "") {
			// console.log("TEST 2")
			const socket = io.connect("http://localhost:5000", {
				// autoConnect: false,
				reconnection: true,
				query: { 'jwt': token },
				// auth: { token: token },
				// transports: ['websocket']
			});

			socket.io.on("error", (error) => {
				window.location.href = "/login";
			});

			socket.io.on("reconnect_failed", () => {
				window.location.href = "/login";
			});


			// socket.emit("message", {'data': 'test!'})

			setSocket(socket);
		}
	}, [token]);

	if (token == null) {
		return (
			<div className="d-flex align-items-center justify-content-center flex-column fullSize">
				<div className="spinner-border" role="status">
					<span className="visually-hidden">Loading...</span>
				</div>
			</div>
		);
	} else {
		return (
			<Router>
				<Nav loggedIn={token !== "" && token !== undefined} removeToken={removeToken}/>
				<Routes>
					<Route path="/login" exact element={
						token !== "" && token !== undefined
							? <Navigate to="/" />
							: <Login setToken={setToken} setRefToken={setRefToken}/>
					} />
					<Route path="/join" exact element={
						token !== "" && token !== undefined
							? <Navigate to="/" />
							: <Join setToken={setToken} setRefToken={setRefToken}/>
					} />

			        <Route path="/" element={
						token === ""
							? <Navigate to="/login" />
							: <div className="d-flex align-items-center justify-content-center flex-column fullSize">
								{ socket ? (
									<Editor socket={socket} token={token} refToken={refToken} setToken={setToken} removeToken={removeToken}/>
								) : (
									<div>Not Connected</div>
								)}
							</div>
			        } />
				</Routes>
			</Router>
		);
	}
}

export default App;