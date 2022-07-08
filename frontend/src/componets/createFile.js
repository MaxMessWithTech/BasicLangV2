import React, { useEffect, useState} from 'react';
import { TextField, Modal } from '@mui/material';
import axios from "axios";

const CreateFile = (props) => {
	const [files, setFiles] = useState([]);
	const [nameField, setNameField] = useState("")
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
				// console.log(response)
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
		// console.log("Open Value Command: " + value);
		if (!files.includes(value)) {
			axios({
				method: "POST",
				url:"/create-file",
				data:{
					fileName: value + ".bsl",
				},
				headers: {
					Authorization: `Bearer ${props.token}`,
				}
			}).then((response) => {
				// console.log(response.data)
				props.socket.emit("load", value + ".bsl");
				handleClose();
				// window.location.href = "/";
			}).catch((error) => {
				if (error.response) {
					// console.log(error.response)
					// console.log(error.response.status)
					// console.log(error.response.headers)
					alert(error.response)
				}
			})
		}
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
						<h5 className="modal-title">Create New File</h5>
						<button type="button" className="btn-close" onClick={handleClose}/>
					</div>
					<div className="modal-body">

						<div className="input-group mb-3">
							<input type="text" className="form-control createFileNameInput " placeholder="New_File_Name"
							       aria-label="New_File_Name" aria-describedby="basic-addon2"
							       value={nameField} onChange={(e) => setNameField(e.target.value)} />
							<span className="input-group-text" id="basic-addon2">.bsl</span>
						</div>
					</div>
					<div className="modal-footer">
						<button type="button" className="btn btn-secondary" onClick={handleClose}>Close</button>
						<button type="button" className="btn btn-primary" onClick={(e) => openFileRequest(nameField)}>Create File</button>
					</div>
				</div>
			</div>
		</Modal>
	);
}

export default CreateFile