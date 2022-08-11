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
let lastCodeVal = "";
let lastSelection = 0;
let changedIndents = false;


function getIndicesOf(searchStr, str, caseSensitive) {
    let searchStrLen = searchStr.length;
    if (searchStrLen === 0) {
        return [];
    }
    let startIndex = 0, index, indices = [];
    if (!caseSensitive) {
        str = str.toLowerCase();
        searchStr = searchStr.toLowerCase();
    }
    while ((index = str.indexOf(searchStr, startIndex)) > -1) {
        indices.push(index);
        startIndex = index + searchStrLen;
    }
    return indices;
}


const Editor = (props) => {
    const [codeValue, setCodeValue] = useState('');
    const codeRef = useRef(null);
    // const [logValue, setLogValue] = useState("");
    const [navValue, setNavValue] = useState(0);

    const [clearDraw, setClearDraw] = useState(false);
    const [currentDrawValues, setCurrentDrawValues] = useState({});

    const socketRef = props.socket

    //socketRef.current.send(JSON.stringify({'command': 'getChildren'}));
    function sendCode() {
        // console.log(JSON.stringify({'command': 'sendCode', 'data': codeValue}))
        // console.log(codeValue);
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
        // console.log("Set Code!")
        // console.log(message);
        props.saveFileName(message['fileName']);
        setCodeValue(message['data']);
        lastCodeVal = message['data'];
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

    const CodeChangeCustom = (e) => {
        // Find all new lines
        const lastIndices = getIndicesOf("\n", lastCodeVal, false)
        // [-1] is there so that the start also counts as a \n
        const curIndices = [-1].concat(getIndicesOf("\n", e.target.value, false));

        // This makes sure the change made is a new line, and that it was added and not removed
        if (lastIndices.length !== curIndices.length && lastIndices.length < curIndices.length - 1) {
            // Find new line indices again so that we still have access to curIndices
            let finalIndex = getIndicesOf("\n", e.target.value, false)

            // Remove all indices that were already in lastIndices
            for (let x = 0; x < lastIndices.length; x++) {
                finalIndex.splice(finalIndex.indexOf(lastIndices[x]), 1);
            }

            // Make sure the 2 indices aren't right next to each other
            // Loop backwards starting at the index before the new line

            let useIndex = curIndices.indexOf(finalIndex[0])

            for (let x = curIndices.indexOf(finalIndex[0]) - 1; x > -1; x--) {
                if (curIndices[x] + 1 !== curIndices[useIndex]) {
                    useIndex = x;
                    break;
                }
            }

            // This gets the last line before the one added
            const lastLine = e.target.value.substring(
                curIndices[useIndex] + 1,
                curIndices[useIndex + 1] + 1
            );

            // Figure out how many tabs should we add to this line
            let lastTab = getIndicesOf("\t", lastLine, false).length;
            // lastTab += getIndicesOf(":", lastLine, false).length;

            // Set the last selection, but add the number of indents
            lastSelection = e.target.selectionStart + lastTab;

            changedIndents = true;

            // Set the code value
            setCodeValue(
                e.target.value.substring(0, curIndices[useIndex] + 1) +
                lastLine +
                "\t".repeat(lastTab) +
                e.target.value.substring(curIndices[useIndex + 1] + 1, e.target.value.length)
            );

            // Stop execution here so that we don't set the value twice
            return
        }

        setCodeValue(e.target.value);
    }

    useEffect(() => {
        if (codeRef.current && changedIndents) {
            codeRef.current['selectionStart'] = lastSelection;
            codeRef.current['selectionEnd'] = lastSelection;
            changedIndents = false;
        }
    }, [codeValue])


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
                        ref={codeRef}
                        onChange={e => CodeChangeCustom(e)}
                        onKeyDown={e => {
                            if (e.key === "Tab") { // tab was pressed

                                // get caret position/selection
                                const val = e.target.value,
                                    start = e.target.selectionStart,
                                    end = e.target.selectionEnd;

                                // set textarea value to: text before caret + tab + text after caret
                                e.target.value = val.substring(0, start) + '\t' + val.substring(end);
                                setCodeValue(e.target.value);

                                // put caret at right position again
                                e.target.selectionStart = e.target.selectionEnd = start + 1;

                                // prevent the focus lose
                                e.preventDefault();
                                return false;

                            }
                            lastCodeVal = e.target.value;
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