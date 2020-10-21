import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';
import { TestComponent } from './testComponent'

function App() {
  var [currentTime, setCurrentTime] = useState("N/A");

  useEffect(() => {
    const interval = setInterval(() => {fetch('/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    })
  }, 1000);
  return () => clearInterval(interval);
}, []);
  
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <TestComponent />
        <p> The date is {currentTime}.</p>
      </header>
    </div>
  );
}

export default App;
