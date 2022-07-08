import React, { useEffect, useState} from 'react';
import Modal from '@mui/material/Modal';
import axios from "axios";

const OpenFile = (props) => {
	const [files, setFiles] = useState([]);
    const handleOpen = () => props.setOpenFile(true);
    const handleClose = () => props.setOpenFile(false);

	useEffect(() => {
		if (props.open) {
			axios({
				method: "POST",
				url: "/get-user-files",
				headers: {
					Authorization: `Bearer ${props.token}`,
				}
			}).then((response) => {
				console.log(response)
				setFiles(response.data)

			}).catch((error) => {
				if (error.response) {
					// console.log(error.response)
					// console.log(error.response.status)
					// console.log(error.response.headers)
				}
			})
		}
	}, [props.open]);

	const openFileRequest = (value) => {
		console.log("Open Value Command: " + value);
		props.socket.emit("load", value);
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
						<h5 className="modal-title">Modal title</h5>
						<button type="button" className="btn-close" onClick={handleClose}/>
					</div>
					<div className="modal-body">
						<ul className="list-group">
							{
								files.map((file) =>
									<li className="list-group-item" key={file.id} onClick={() => openFileRequest(file.file)}>{file.file}</li>
								)
							}
						</ul>
					</div>
				</div>
			</div>
		</Modal>
	);
}

export default OpenFile