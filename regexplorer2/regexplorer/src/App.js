import React from 'react';
import './App.css';

function CreateTextbox(props) {
  return (
    <div className="textboxContainer">
      <label for="textbox">Your Text Here</label>
      <textarea id="textbox" onChange={props.handleTextChange}  />
      <p>Input: {props.text}</p>
    </div>
  );
}

function CreateRegexbox(props) {
  return (
    <div className="regexboxContainer">
      <label for="regexbox">Regular Expression</label>
      <input id="regexbox" onChange={props.handleRegexChange}  />
      <p>Regex: {props.regex}</p>
    </div>
  );
}

function CreateOutputbox(props) {
  return (
    <div className="outputboxContainer">
      <label for="outputbox">Output</label>
      <div className="container">
        <p id="outputbox">Output: {props.output}</p>
      </div>
    </div>
  );
}

function CreateHeader(props) {
  return (
    <div className="headerContainer">
      <h1>RegExplorer</h1>
    </div>
  )
}

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      text: '',
      regex: '',
      output: 'hello'
    };
    this.handleTextChange = this.handleTextChange.bind(this);
    this.handleRegexChange = this.handleRegexChange.bind(this);
  }

  handleTextChange(event) {
    this.setState({text: event.target.value});
    let output
    try {
      let re= new RegExp(this.state.regex)
      output = re.exec(event.target.value)
    }
    catch(err) {
      output = "Error"
    }
    this.setState({output: output})
  }
  handleRegexChange(event) {
    this.setState({regex: event.target.value});
    let output
    try {
      let re= new RegExp(event.target.value)
      output = re.exec(this.state.text)
    }
    catch(err) {
      output = "Error"
    }
    this.setState({output: output})
  }

  render() {
    return(
      <div>
        <div><CreateHeader /></div>
        <div className="leftbox">
          <CreateTextbox text={this.state.text} handleTextChange={this.handleTextChange} />
        </div>
        <div className="rightbox">
          <CreateRegexbox regex={this.state.regex} handleRegexChange={this.handleRegexChange}/>
          <CreateOutputbox output={this.state.output} />
        </div>
      </div>
    )
  }
}

export default App;
