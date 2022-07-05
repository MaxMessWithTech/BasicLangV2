import React, { Component } from "react";
import { render } from "react-dom";
import Editor from "./Editor";

export default class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="d-flex align-items-center justify-content-center fullSize">
        <Editor />
      </div>
    );
  }
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);
