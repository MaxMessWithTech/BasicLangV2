import React, { useRef, useEffect, useState} from 'react';
import Canvas from './Canvas.js';
import greenFlag from './greenFlag.svg';
import redStop from './redStop.svg';
import EditorCSS from './Editor.css';

import {
    ReflexContainer,
    ReflexSplitter,
    ReflexElement
} from 'react-reflex'

import 'react-reflex/styles.css'
import io from "socket.io-client";

let Convert = require('ansi-to-html');
let convert = new Convert();

let firstUpdate = true;
let currentLogValue = "";
let isCtrl = false;
let sKeyPress = false;
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

        socketRef.emit("sendCode", codeValue);

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
        socketRef.emit("message", JSON.stringify({'command': 'stopRun', 'data': ''}));
    }

    function setNavValueWithUpdate(numb) {
        setNavValue(numb)
        if (numb === 0 && currentLogValue !== "") {
            setTimeout(() => { document.getElementById("log").innerHTML = currentLogValue; }, 1);
        }
    }

    const openWebsocket = () => {
        console.log('open');
        socketRef.emit("load");
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
        console.log("NEW Draw Command");
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
        setCodeValue(message);
    }

    useEffect(() => {
        socketRef.on('setCode', setCodeHandler);
        return () => {
          socketRef.off('setCode', setCodeHandler);
        }
    }, []);

    if (firstUpdate) {
        openWebsocket();
    }

    const onKeyPress = (e) => {
        if (e.key === "Meta") {
            e.preventDefault();
            isCtrl = true;
        } else if (e.key === "Control") {
            e.preventDefault();
            isCtrl = true;
        } else if (e.key === "s" && isCtrl && !sKeyPress){
            sKeyPress = true;
            e.preventDefault();

            console.log("SAVE!!")

            socketRef.emit("save", codeValue);
        }
    }

    document.addEventListener('keydown', onKeyPress);
    document.addEventListener('keyup', function(e){
        if(e.key === "Meta" && isCtrl) {
            e.preventDefault();
            isCtrl = false;
        } else if (e.key === "Control" && isCtrl) {
            e.preventDefault();
            isCtrl = false;
        } else if (e.key === "s" && sKeyPress) {
            sKeyPress = false;
            console.log("S Key Up")
            e.preventDefault();
        }
    });


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
        <ReflexContainer className="d-flex align-items-center justify-content-center fullSize" orientation="vertical" windowResizeAware={true}>
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
            </ReflexElement>
            <ReflexSplitter/>
            <ReflexElement className="d-flex flex-column align-items-center justify-content-center sideBox" flex={0.2}>
                <div className="p-2 d-flex align-items-center justify-content-between controls" id="sideBoxControls">
                    <button className="runBtnBtn"><img id="RunBtn" className="runBtn" onClick={sendCode} src={greenFlag} alt={"Run"}/></button>
                    <img id="StopBtn" className="runBtn" onClick={sendStop} src={redStop} alt={"Stop"}/>
                </div>
                <div className="d-flex align-items-center justify-content-center customNav">
                    <div className="btn-group marginNav" role="group" aria-label="Third group">
                        <button type="button" className={navValue === 0 ? "btn btn-primary" : "btn btn-secondary"} onClick={(e) => setNavValueWithUpdate(0)}>Log</button>
                    </div>
                    <div className="btn-group marginNav" role="group" aria-label="Third group">
                        <button type="button" className={navValue === 1 ? "btn btn-primary" : "btn btn-secondary"} onClick={(e) => setNavValueWithUpdate(1)}>Output</button>
                    </div>
                </div>
                <div className="p-2 d-flex flex-column align-items-center justify-content-center" id="sideBoxLog">
                    <p id="log" style={{display: navValue === 0 ? 'block' : 'none'}}> </p>
                    <div id="canvas" style={{display: navValue === 0 ? 'none' : 'block'}}><Canvas draw={draw} socket={props.socket}/></div>
                </div>
            </ReflexElement>
        </ReflexContainer>
    );
}

export default Editor;