import React, { useEffect, useState} from 'react';
import { TextField, Modal } from '@mui/material';
import axios from "axios";

const PackageManager = (props) => {
	const [packages, setPackages] = useState([]);
    const handleOpen = () => props.setOpen(true);
    const handleClose = () => props.setOpen(false);

	useEffect(() => {
		if (props.open) {
			axios({
				method: "POST",
				url: "/get-packages",
				headers: {
					Authorization: `Bearer ${props.token}`,
				}
			}).then((response) => {
				// console.log(response)
				setPackages(response.data)

			}).catch((error) => {
				if (error.response) {
					// console.log(error.response)
					// console.log(error.response.status)
					// console.log(error.response.headers)
				}
			})
		}
	}, [props.open]);

	const addPackage = (value) => {

	};

	return (
		<Modal
			open={props.open}
			onClose={handleClose}
	        aria-labelledby="modal-modal-title"
	        aria-describedby="modal-modal-description"
		>
			<div className="modal-dialog">
				<div className="modal-content">
					<div className="modal-header">
						<h5 className="modal-title">Open File</h5>
						<button type="button" className="btn-close" onClick={handleClose}/>
					</div>
					<div className="modal-body">
						<ul className="list-group">
							{
								packages.map((_package) =>
									<li className="list-group-item" key={_package.id} onClick={() => addPackage(_package._package)}>{_package._package}</li>
								)
							}
						</ul>
					</div>
				</div>
			</div>
		</Modal>
	);
}

export default PackageManager