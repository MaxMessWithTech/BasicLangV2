import { useState } from 'react';

function useFile() {

	function getFile() {
		let _fileName = localStorage.getItem('fileName');
		if (!_fileName) {
			_fileName = "script.bsl"
		}
		return _fileName && _fileName
	}

	const [fileName, setFileName] = useState(getFile());

	function saveFileName(_fileName) {
		localStorage.setItem('fileName', _fileName);
		setFileName(_fileName);
	}

	function removeFileName() {
		localStorage.removeItem("fileName");
		setFileName("script.bsl");
	}

	return {
		saveFileName,
		fileName,
		removeFileName
	}

}

export default useFile;
