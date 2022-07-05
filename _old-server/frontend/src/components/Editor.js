import React, { useRef, useEffect, useState } from 'react';
import ReconnectingWebSocket from './reconnecting-websocket.js';
import {IconButton} from "@mui/material";
import Canvas from './Canvas.js';

var Convert = require('ansi-to-html');
var convert = new Convert();

import {
    ReflexContainer,
    ReflexSplitter,
    ReflexElement
} from 'react-reflex'

var firstUpdate = true;

var defultBSLCode = "func:\r\n"                                                     +
                    "\tprint(\"hello\")\r\n"                                        +
                    "\tif (testVar==\"Max\"):\r\n"                                  +
                    "\t\tprint (\"hello Max!!!!\")\r\n"                             +
                    "\t\tif (true == false):\r\n"                                   +
                    "\t\t\tprint(\"TRUE\")\r\n"                                     +
                    "\t\telse:\r\n"                                                 +
                    "\t\t\tprint(\"FALSE\")\r\n"                                    +
                    "\telse:\r\n"                                                   +
                    "\t\tprint(\"Hello \" + testVar)\r\n"                           +

                    "loopTest:\r\n"                                                 +
                    "\trepeat(10 * 0.5):\r\n"                                       +
                    "\tprint(\"Loop\")\r\n"                                         +
                    "\ttestNumb = 0\r\n"                                            +
                    "\trepeatUntil(testNumb == 10):\r\n"                            +
                    "\t\tprint(\"Loop2\")\r\n"                                      +
                    "\t\ttestNumb = testNumb + 1\r\n"                               +
                    "\t\tdrawLine(testNumb, 0, testNumb, 100)\r\n"                  +

                    "run:\r\n"                                                      +
                    "\t# func()\r\n"                                                +
                    "\t# testVar4 = testVar\r\n"                                    +
                    "\ttestVar = \"Max\"\r\n"                                       +
                    "\ttestVar2 = 123\r\n"                                          +
                    "\ttestVar3 = testVar + \" Miller\"\r\n"                        +
                    "\tprint(\"Test Var: \" + testVar + \" \" + testVar3)\r\n"      +
                    "\tsleep(1)\r\n"                                                +
                    "\tfunc()\r\n"                                                  +
                    "\tloopTest()\r\n"                                              +
                    "\tprint(\"End\")\r\n";

var currentLogValue = "";
var isCtrl = false;
var sKeyPress = false;

const Editor = () => {
    const [codeValue, setCodeValue] = useState("");
    const [logValue, setLogValue] = useState();
    const [navValue, setNavValue] = useState(0);

    const [doDraw, setDoDraw] = useState(false);
    const [currentDrawValue, setCurrentDrawValue] = useState({});

    const socketRef = useRef();

    //socketRef.current.send(JSON.stringify({'command': 'getChildren'}));
    function sendCode() {
        // console.log(JSON.stringify({'command': 'sendCode', 'data': codeValue}))
        setCurrentDrawValue({'type': 'clear'});
        setDoDraw(true);

        socketRef.current.send(JSON.stringify({'command': 'sendCode', 'data': codeValue}));
    }

    function sendStop() {
        console.log("STOP RUN!!")
        socketRef.current.send(JSON.stringify({'command': 'stopRun', 'data': ''}));
    }

    function setNavValueWithUpdate(numb) {
        setNavValue(numb)
        if (numb == 0 && currentLogValue != "") {
            setTimeout(() => { document.getElementById("log").innerHTML = currentLogValue; }, 1);
        }
    }

    const openWebsocket = () => {
        socketRef.current = new ReconnectingWebSocket('ws://'+ window.location.host + "/ws/main/")
        socketRef.current.onopen = e => {
            console.log('open', e);
            socketRef.current.send(JSON.stringify({'command': 'load'}));
        }
        socketRef.current.onmessage = e => {
            var jsonBaseData = JSON.parse(e.data);
            // console.log(jsonBaseData);
            var type = jsonBaseData['type'];
            if (type == "run") {
                var data = jsonBaseData['data']
                var dataType = data['type']

                if (dataType == "log") {
                    var logData = data['data']
                    for (let x = 0; x < logData.length; x++) {
                        if (currentLogValue == "")
                            currentLogValue = convert.toHtml(logData[x])
                        else
                            currentLogValue = currentLogValue + "<br/>" + convert.toHtml(logData[x])
                        setLogValue(currentLogValue)

                        if (navValue == 0) {
                            try {
                                document.getElementById("log").innerHTML = currentLogValue
                            } catch (error) {}
                        }
                    }
                } else if (dataType == "drawLine") {
                    // console.log(jsonBaseData)
                    var startX  = data['data']['startX']
                    var startY  = data['data']['startY']
                    var endX    = data['data']['endX']
                    var endY    = data['data']['endY']
                    setCurrentDrawValue({
                        'type': 'drawLine',
                        'startX': startX,
                        'startY': startY,
                        'endX': endX,
                        'endY': endY,
                    });
                    setDoDraw(true);
                }

            } else if (type == "clearLog") {
                currentLogValue = "";
                setLogValue(currentLogValue);
                if (navValue == 0) {
                    try {
                        document.getElementById("log").innerHTML = currentLogValue
                    } catch (error) {}
                }
            } else if (type == "setCode") {
                setCodeValue(jsonBaseData['data'])
            }
        }

        socketRef.current.onerror = e => {
            console.log('error', e)
        }
        firstUpdate = false;
    }

    if (firstUpdate) {
        openWebsocket();
    }

    const onKeyPress = (e) => {
        if (e.which == 91) {
            e.preventDefault();
            isCtrl = true;
        } else if (e.which == 93) {
            e.preventDefault();
            isCtrl = true;
        } else if (e.which == 83 && isCtrl && !sKeyPress){
            sKeyPress = true;
            e.preventDefault();

            console.log("SAVE!!")

            socketRef.current.send(JSON.stringify({'command': 'save', 'data': codeValue}));
        }
    }
    document.addEventListener('keydown', onKeyPress);
    document.addEventListener('keyup', function(e){
        if(e.which == 91 && isCtrl) {
            e.preventDefault();
            isCtrl = false;
        } else if (e.which == 93 && isCtrl) {
            e.preventDefault();
            isCtrl = false;
        } else if (e.which == 83 && sKeyPress) {
            sKeyPress = false;
            console.log("S Key Up")
            e.preventDefault();
        }
    });


    const draw = () => {
        if (doDraw) {
            setDoDraw(false);
            return currentDrawValue;
        }
        return {'type': ''}
    }

    return (
        <ReflexContainer className="d-flex align-items-center justify-content-center fullSize" orientation="vertical">
            <ReflexElement className="d-flex align-items-center justify-content-center codeBox" >
                <textarea
                    id="codeEditorTextField"
                    value={codeValue}
                    onChange={e => setCodeValue(e.target.value)}
                    onKeyDown={e => {
                        // console.log(e)
                        if (e.key == 9) { // tab was pressed

                            // get caret position/selection
                            var val = e.target.value,
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
            <ReflexElement className="d-flex flex-column align-items-center justify-content-center sideBox" >
                <div className="p-2 d-flex align-items-center justify-content-center" id="sideBoxControls">
                    <img id="RunBtn" src="/static/images/greenFlag.svg" onClick={sendCode}/>
                    <img id="RunBtn" src="/static/images/redStop.svg" onClick={sendStop}/>
                </div>
                <div className="p-2 d-flex flex-column align-items-center justify-content-center" id="sideBoxLog">
                    <div className="d-flex align-items-center justify-content-center customNav">
                        <div className="btn-group marginNav" role="group" aria-label="Third group">
                            <button type="button" className={navValue == 0 ? "btn btn-primary" : "btn btn-secondary"} onClick={(e) => setNavValueWithUpdate(0)}>Log</button>
                        </div>
                        <div className="btn-group marginNav" role="group" aria-label="Third group">
                            <button type="button" className={navValue == 1 ? "btn btn-primary" : "btn btn-secondary"} onClick={(e) => setNavValueWithUpdate(1)}>Output</button>
                        </div>
                    </div>

                    <p id="log" style={{display: navValue == 0 ? 'block' : 'none'}}>{logValue}</p>
                    <div id="canvas" style={{display: navValue == 0 ? 'none' : 'block'}}><Canvas draw={draw}/></div>
                </div>
            </ReflexElement>
        </ReflexContainer>
    );
}

export default Editor;