import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to RegExplorer</h1>
        </header>
        <div class="container">
          <div class="row">
            <div class="col-sm-6">
              <h2>Insert Raw Text Here!</h2>
              <div class="container">
                <input className="raw-text-input" type="text" placeholder="testing"></input>
              </div>
            </div>
            <div class="col-sm-6">
              <h2>Right Side</h2>
              <div class="container">
                <input className="regex-input" type="text" placeholder="regex"></input>
                <p className="regex-output"> Output </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
