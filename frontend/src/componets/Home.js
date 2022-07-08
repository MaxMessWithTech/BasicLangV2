import React, { useEffect, useState } from 'react';
import BasicLangLogo from './BasicLangLogo.svg'
import './Home.css';

const Home = (props) => {
	return (
		<div className="d-flex align-items-center justify-content-center flex-column homeWindow gradient-custom">
			<div className="card bg-dark text-white HomeCard" style={{borderRadius: '1rem'}}>
				<div className="d-flex align-items-center justify-content-center flex-column">
					<img className="logoHome" src={BasicLangLogo} alt={"Basic Lang Web"}/>
					<h3>Created By: Max Miller</h3>
					<p>This page is still under construction... please visit my <a href="https://github.com/MaxMessWithTech/BasicLangV2">github page</a></p>
				</div>
			</div>
		</div>
	);
}

export default Home