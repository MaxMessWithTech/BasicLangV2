import React, { useRef, useEffect, useState} from 'react';
import { TextField, Icon } from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelIcon from '@mui/icons-material/Cancel';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import axios from "axios";
import './join.css'
import BasicLangJoinLogo from "./BasicLangJoinLogo.svg";

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

const Join = (props) => {

	const [name, setName] = useState("");
	const [nameError, setNameError] = useState(false);

	const [email, setEmail] = useState("");
	const [emailError, setEmailError] = useState(false);
	const [emailExistsError, setEmailExistsError] = useState(false)

	const [password, setPassword] = useState("");
	const [passwordErrors, setPasswordErrors] = useState({
		'letter': true,
		'capital': true,
		'number': true,
		'length': true,
		'any': false
	});


	const [confPassword, setConfPassword] = useState("");

	function ValidateEmail(input) {
		const validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+$/;

		return input.match(validRegex);
	}

	const sendAPI = () => {
		setEmailExistsError(false)
		axios({
			method: "POST",
			url:"/join",
			data:{
				email: email,
				password: password,
				name: name
			}
		}).then((response) => {
			// console.log(response.data)
			props.setRefToken(response.data.refresh_token);
			props.setToken(response.data.access_token);
			// window.location.href = "/";
		}).catch((error) => {
			if (error.response) {
				if (error.response.data.msg === 'User Already Exists') { setEmailExistsError(true); }
				else {
					console.log(error.response)
				}
			}
		})
	}

	const btnClick = (e) => {
		let error = false;
		if (name === "") { setNameError(true); error = true; }
		if (!ValidateEmail(email)) { setEmailError(true); error = true; }
		if (passwordErrors.letter || passwordErrors.capital || passwordErrors.number || passwordErrors.length) {
			setPasswordErrors({
				'letter': passwordErrors.letter,
				'capital': passwordErrors.capital,
				'number': passwordErrors.number,
				'length': passwordErrors.length,
				'any': true
			});
			error = true;
		}

		if (!error) {
			sendAPI();
		}

		e.preventDefault()
	}

	const changePassword = (val) => {
		let errors = {
			'letter': false,
			'capital': false,
			'number': false,
			'length': false,
			'any': false
		};
		 // Validate lowercase letters
		let lowerCaseLetters = /[a-z]/g;
		errors.letter = !val.match(lowerCaseLetters);

		// Validate capital letters
		let upperCaseLetters = /[A-Z]/g;
		errors.capital = !val.match(upperCaseLetters);

		// Validate numbers
		let numbers = /[0-9]/g;
		errors.number = !val.match(numbers);

		// Validate length
		errors.length = val.length < 8;

		if (!(errors.letter || errors.capital || errors.number || errors.length) && passwordErrors.any) {
			errors.any = false;
		}

		setPasswordErrors(errors);
		setPassword(val);
	}

	const changeName = (val) => {
		if (nameError && val !== "") { setNameError(false); }
		setName(val)
	}

	const changeEmail = (val) => {
		if (emailError && ValidateEmail(val)) { setEmailError(false); }
		setEmail(val)
	}

	return(
		<ThemeProvider theme={darkTheme}><section className="gradient-custom">
			<div className="container py-5 h-100">
				<div className="row d-flex justify-content-center align-items-center h-100">
					<div className="col-12 col-md-8 col-lg-6 col-xl-5">
						<div className="card bg-dark text-white" style={{borderRadius: '1rem'}}>
							<div className="card-body p-5 text-center">
								<div className="mb-md-2 mt-md-2 pb-2">
									<img className="mb-3 logoJoin" src={BasicLangJoinLogo} alt={"Basic Lang Web"}/>

									{
										nameError
											? <TextField
												className="mb-3 customInput"
												value={name}
												onChange={e => changeName(e.target.value)}
												label="Your Name"
												variant="outlined"
												error
											/>
											: <TextField
												className="mb-3 customInput"
												value={name}
												onChange={e => changeName(e.target.value)}
												label="Your Name"
												variant="outlined"
											/>
									}

									{
										emailError
											? <TextField
												className="mb-3 customInput"
												value={email}
												onChange={e => changeEmail(e.target.value)}
												label="Email"
												variant="outlined"
												error
											/>
											: <TextField
												className="mb-3 customInput"
												value={email}
												onChange={e => changeEmail(e.target.value)}
												label="Email"
												variant="outlined"
											/>
									}

									{
										passwordErrors.any
											? <TextField
												className="mb-3 customInput"
												value={password}
												onChange={e => changePassword(e.target.value)}
												label="Password"
												type="password"
												error
											/>
											: <TextField
												className="mb-3 customInput"
												value={password}
												onChange={e => changePassword(e.target.value)}
												label="Password"
												type="password"
											/>
									}

									{
										passwordErrors.any
											? <TextField
												className="mb-4 customInput"
												value={confPassword}
												onChange={e => setConfPassword(e.target.value)}
												label="Repeat Your Password"
												type="password"
												error
											/>
											: <TextField
												className="mb-4 customInput"
												value={confPassword}
												onChange={e => setConfPassword(e.target.value)}
												label="Repeat Your Password"
												type="password"
											/>
									}

									<div className="d-flex justify-content-center align-items-start flex-column">
									{
										password === confPassword
											? <p className="mb-1"><Icon component={CheckCircleIcon} color="success"/> Passwords Match</p>
											: <p className="mb-1"><Icon component={CancelIcon} color="error"/> Passwords Don't Match</p>
									}
									{
										!passwordErrors.letter
											? <p className="mb-1"><Icon component={CheckCircleIcon} color="success"/> A lowercase letter</p>
											: <p className="mb-1"><Icon component={CancelIcon} color="error"/> A lowercase letter</p>
									}
									{
										!passwordErrors.capital
											? <p className="mb-1"><Icon component={CheckCircleIcon} color="success"/> A capital (uppercase) letter</p>
											: <p className="mb-1"><Icon component={CancelIcon} color="error"/> A capital (uppercase) letter</p>
									}
									{
										!passwordErrors.number
											? <p className="mb-1"><Icon component={CheckCircleIcon} color="success"/> A number</p>
											: <p className="mb-1"><Icon component={CancelIcon} color="error"/> A number</p>
									}
									{
										!passwordErrors.length
											? <p className="mb-4"><Icon component={CheckCircleIcon} color="success"/> Minimum 8 characters</p>
											: <p className="mb-4"><Icon component={CancelIcon} color="error"/> Minimum 8 characters</p>
									}
									</div>

									<button className="btn btn-outline-light btn-lg px-5" type="submit" onClick={e => btnClick(e)}>Join</button>

								</div>

								<div>
									<p className="mb-0">Already have an account? <a href="/login" className="text-white-50 fw-bold">Login</a></p>
								</div>

							</div>
						</div>
					</div>
				</div>
			</div>
			{
				emailExistsError
					? <div className="alert alert-danger d-flex align-items-center alert-dismissible customAlert" role="alert">
						<div>
							A user with that email already exists
						</div>
						<button type="button" className="btn-close" onClick={(e) => setEmailExistsError(false)}/>
					</div>
					: null
			}
		</section></ThemeProvider>
	);
}

// <p className="small mb-5 pb-lg-2"><a className="text-white-50" href="#">Forgot
// 										password?</a></p>

export default Join