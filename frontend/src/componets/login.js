import React, { useRef, useEffect, useState} from 'react';
import axios from "axios";
import './login.css'

const Login = (props) => {

	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");

	const btnClick = (e) => {
		axios({
			method: "POST",
			url:"/token",
			data:{
				email: email,
				password: password
			}
		}).then((response) => {
			props.setToken(response.data.access_token);
			window.location.href = "/";
		}).catch((error) => {
			if (error.response) {
				console.log(error.response)
				console.log(error.response.status)
				console.log(error.response.headers)
			}
		})

		// setEmail("");
		// setPassword("");

		e.preventDefault()
	}

	return(
		<section className="gradient-custom">
			<div className="container py-5 h-100">
				<div className="row d-flex justify-content-center align-items-center h-100">
					<div className="col-12 col-md-8 col-lg-6 col-xl-5">
						<div className="card bg-dark text-white" style={{borderRadius: '1rem'}}>
							<div className="card-body p-5 text-center">

								<div className="mb-md-5 mt-md-4 pb-5">

									<h2 className="fw-bold mb-2 text-uppercase">Login</h2>
									<p className="text-white-50 mb-5">Please enter your login and password!</p>

									<div className="form-floating form-white mb-3 customInput">
										<input type="email" className="form-control customInput" id="typeEmailX"
										       placeholder="name@example.com" value={email} onChange={e => setEmail(e.target.value)}/>
										<label htmlFor="typeEmailX">Email</label>
									</div>

									<div className="form-floating form-white mb-3 customInput">
										<input type="password" id="typePasswordX"
										       className="form-control form-control-lg customInput" placeholder="********"
										       value={password} onChange={e => setPassword(e.target.value)}/>
										<label htmlFor="typePasswordX">Password</label>
									</div>

									<button className="btn btn-outline-light btn-lg px-5" type="submit" onClick={e => btnClick(e)}>Login</button>

								</div>

								<div>
									<p className="mb-0">Don't have an account? <a href="join" className="text-white-50 fw-bold">Sign Up</a></p>
								</div>

							</div>
						</div>
					</div>
				</div>
			</div>
		</section>
	);
}

// <p className="small mb-5 pb-lg-2"><a className="text-white-50" href="#">Forgot
// 										password?</a></p>

export default Login