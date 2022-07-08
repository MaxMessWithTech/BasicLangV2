import React, { useRef, useEffect, useState} from 'react';
import Canvas from './Canvas.js';
import greenFlag from './greenFlag.svg';
import redStop from './redStop.svg';
import './Editor.css';
import Nav from './nav';

import {
    ReflexContainer,
    ReflexSplitter,
    ReflexElement
} from 'react-reflex'

import 'react-reflex/styles.css'
import io from "socket.io-client";
import axios from "axios";

let Convert = require('ansi-to-html');
let convert = new Convert();

let firstUpdate = true;
let currentLogValue = "";
let isCtrl = false;
let sentSave = false;
let currentDrawIndex = 0;


const Editor = (props) => {
    const [codeValue, setCodeValue] = useState('');
    // const [logValue, setLogValue] = useState("");
    const [navValue, setNavValue] = useState(0);

    const [clearDraw, setClearDraw] = useState(false);
    const [currentDrawValues, setCurrentDrawValues] = useState({});

    const socketRef = props.socket

    //socketRef.current.send(JSON.stringify({'command': 'getChildren'}));
    function sendCode() {
        // console.log(JSON.stringify({'command': 'sendCode', 'data': codeValue}))
        setCurrentDrawValues([]);
        setClearDraw(true);

        socketRef.emit("sendCode", codeValue, props.fileName);

        currentLogValue = "";
        //setLogValue(currentLogValue);
        if (navValue === 0) {
            try {
                document.getElementById("log").innerHTML = currentLogValue;
            } catch (error) {}
        }
    }

    function sendStop() {
        console.log("STOP RUN!!")
        socketRef.emit("message", JSON.stringify({'command': 'stopRun', 'data': ''}), props.fileName);
    }

    function setNavValueWithUpdate(numb) {
        setNavValue(numb)
        if (numb === 0 && currentLogValue !== "") {
            setTimeout(() => { document.getElementById("log").innerHTML = currentLogValue; }, 1);
        }
    }

    const openWebsocket = () => {
        console.log('open');
        socketRef.emit("load", props.fileName);
        firstUpdate = false;
    }

    const logHandler = (message) => {
        if (currentLogValue === "") {currentLogValue = convert.toHtml(message);}
        else {currentLogValue = currentLogValue + `<br/>` + convert.toHtml(message);}

        // setLogValue(currentLogValue);

        if (navValue === 0) {
            try {
                document.getElementById("log").innerHTML = currentLogValue;
            } catch (error) {
            }
        }
    }

    useEffect(() => {
        socketRef.on('log', logHandler);
        return () => {
            socketRef.off('log', logHandler);
        }
    }, []);

    const drawHandler = (message) => {
        //console.log("NEW Draw Command");
        const data = JSON.parse(message);

        setCurrentDrawValues(oldArray => [...oldArray, {
            'type': 'draw',
            'pts': data['cords'],
            'color': data['color']
        }]);
        // setDoDraw(true);
        /*
        const startX = data['data']['startX'];
        const startY  = data['data']['startY']
        const endX    = data['data']['endX']
        const endY    = data['data']['endY']
        setCurrentDrawValue({
            'type': 'drawLine',
            'startX': startX,
            'startY': startY,
            'endX': endX,
            'endY': endY,
        });
         */
        // setDoDraw(true);
    }

    useEffect(() => {
        socketRef.on('draw', drawHandler);
        return () => {
            socketRef.off('draw', drawHandler);
        }
    }, []);

    const clearLogHandler = (message) => {
        currentLogValue = "";
        // setLogValue(currentLogValue);
        if (navValue === 0) {
            try {
                document.getElementById("log").innerHTML = currentLogValue
            } catch (error) {}
        }
    }

    useEffect(() => {
        socketRef.on('clearLog', clearLogHandler);
        return () => {
            socketRef.off('clearLog', clearLogHandler);
        }
    }, []);

    const setCodeHandler = (message) => {
        console.log("Set Code!")
        props.saveFileName(message['fileName']);
        setCodeValue(message['data']);
    }

    useEffect(() => {
        socketRef.on('setCode', setCodeHandler);
        return () => {
          socketRef.off('setCode', setCodeHandler);
        }
    }, []);

    function pollServer() {
        axios({
			method: "POST",
			url:"/refresh-token",
			headers:{
				Authorization: `Bearer ${props.refToken}`,
			}
		}).then((response) => {
            if (response.status === 202) {
                console.log(response.data.access_token)
                console.log(response.data.access_token !== props.token)
                props.setToken(response.data.access_token)
            }

		}).catch((error) => {
			if (error.response) {
				// console.log(error.response)
				// console.log(error.response.status)
				// console.log(error.response.headers)
                props.removeToken();
			}
		})
        setTimeout(()=> pollServer(), 1800000);
    }

    function sendSave() {
        socketRef.emit("save", document.getElementById("codeEditorTextField").value, props.fileName);
    }

    if (firstUpdate) {
        openWebsocket();
        setTimeout(()=> pollServer(), 1000);
    }

    document.onkeydown = (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            sendSave();
        }
    }



    const draw = () => {
        if (currentDrawValues.length > 0 && currentDrawIndex < currentDrawValues.length) {
            let val = currentDrawValues[currentDrawIndex]
            currentDrawIndex += 1;
            return val;
        }
        if (clearDraw) {
            setClearDraw(false);
            currentDrawIndex = 0;
            return {'type': 'clear'}
        }
        return {'type': ''}
    }

    return (
        <div className="d-flex align-items-center justify-content-center flex-column editorWindow">
            <ReflexContainer className="d-flex align-items-center justify-content-center editorWindow" orientation="vertical" windowResizeAware={true}>
                <ReflexElement className="d-flex align-items-center justify-content-center codeBox" minSize={window.innerWidth * 0.2} maxSize={window.innerWidth * 0.8}>
                    <textarea
                        id="codeEditorTextField"
                        className="codeEditorTextField"
                        value={codeValue}
                        onChange={e => setCodeValue(e.target.value)}
                        onKeyDown={e => {
                            // console.log(e)
                            if (e.key === "Tab") { // tab was pressed

                                // get caret position/selection
                                const val = e.target.value,
                                    start = e.target.selectionStart,
                                    end = e.target.selectionEnd;

                                // set textarea value to: text before caret + tab + text after caret
                                e.target.value = val.substring(0, start) + '\t' + val.substring(end);

                                // put caret at right position again
                                e.target.selectionStart = e.target.selectionEnd = start + 1;

                                // prevent the focus lose
                                e.preventDefault();
                                return false;

                            }
                        }}
                        autoCapitalize="none"
                        autoComplete="none"
                        autoCorrect="none"
                        data-gramm_editor="false"
                        autoFocus
                    />
                    <div className="fileDisplay">{props.fileName}</div>
                </ReflexElement>
                <ReflexSplitter/>
                <ReflexElement className="d-flex flex-column align-items-center justify-content-center sideBox" flex={0.2}>
                    <div className="p-2 d-flex align-items-center justify-content-between controls">

                        <div className="p-2 d-flex align-items-center justify-content-center">
                            <button className="runBtnBtn"><img id="RunBtn" className="runBtn" onClick={sendCode} src={greenFlag} alt={"Run"}/></button>
                            <button className="runBtnBtn"><img id="StopBtn" className="runBtn" onClick={sendStop} src={redStop} alt={"Stop"}/></button>
                        </div>

                        <div className="p-2 d-flex align-items-center justify-content-between">
                            <div className="btn-group marginNav " role="group" aria-label="Third group">
                                <button type="button" className={navValue === 0 ? "btn btn-primary" : "btn btn-secondary"} onClick={(e) => setNavValueWithUpdate(0)}>Log</button>
                            </div>
                            <div className="btn-group marginNav selectBtn" role="group" aria-label="Third group">
                                <button type="button" className={navValue === 1 ? "btn btn-primary" : "btn btn-secondary"} onClick={(e) => setNavValueWithUpdate(1)}>Output</button>
                            </div>
                        </div>

                    </div>
                    <div className="p-2 d-flex flex-column align-items-center justify-content-center" id="sideBoxLog">
                        <p id="log" style={{display: navValue === 0 ? 'block' : 'none'}}> </p>
                        <div id="canvas" style={{display: navValue === 0 ? 'none' : 'block'}}><Canvas draw={draw} socket={props.socket}/></div>
                    </div>
                </ReflexElement>
            </ReflexContainer>
        </div>
    );
}

export default Editor;