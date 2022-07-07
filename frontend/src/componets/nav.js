import React, { useRef, useEffect, useState} from 'react';
import axios from "axios";
import './nav.css';
import BasicLangLogo from './BasicLangLogo.svg'

const Nav = (props) => {

	function logMeOut() {
		console.log("Post")
		axios({
			method: "POST",
			url:"/logout",
		}).then((response) => {
			props.removeToken();
			window.location.href = "/login"
		}).catch((error) => {
			if (error.response) {
				console.log(error.response);
				console.log(error.response.status);
				console.log(error.response.headers);
			}
		})
	}
	// console.log(props.loggedIn);


	return (
		<nav className="navbar navbar-expand-sm bg-dark navbar-dark customNavbar">
			<ul className="container-fluid justify-content-start customULNav">
				<a className="navbar-brand" href="/"><img className="logo" src={BasicLangLogo} alt={"Basic Lang Web"}/></a>

				<ul className="navbar-nav">
					<li className="nav-item dropdown">
						<a className="nav-link dropdown-toggle" id="navbarScrollingDropdown" role="button"
						   data-bs-toggle="dropdown" aria-expanded="false">
							File
						</a>
						<ul className="dropdown-menu" aria-labelledby="navbarScrollingDropdown">
							<li><a className="dropdown-item" >Open</a></li>
							<li><a className="dropdown-item" >Save As</a></li>
							<li><a className="dropdown-item" >Save</a></li>
							<li>
								<hr className="dropdown-divider" />
							</li>
							<li><a className="dropdown-item" >Something else here</a></li>
						</ul>
					</li>
				</ul>
			</ul>
			<ul className="container-fluid justify-content-end customULNav">
				{
					props.loggedIn
						? <ul className="navbar-nav">
							<li className="nav-item">
								<a className="nav-link active" href="#" onClick={logMeOut}>Logout</a>
							</li>
						</ul>
						: <ul className="navbar-nav">
							<li className="nav-item">
								<a className="nav-link active" href="/join">Join</a>
							</li>
							<li className="nav-item">
								<a className="nav-link active" href="/login">Login</a>
							</li>
						</ul>
				}
			</ul>
		</nav>
	);
}

export default Nav