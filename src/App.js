import React, { Component } from 'react';
import './App.css';
import Calendar2 from "./components/Calendar2.js";

class App extends Component {
  render() {
    return (
      <div className="App">
      <h1>Calendar Scheduler App</h1>
        <Calendar2 />
      </div>
    );
  }
}

export default App;
