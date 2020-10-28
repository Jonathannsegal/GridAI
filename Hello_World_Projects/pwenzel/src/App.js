import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';
import { TestComponent } from './testComponent'
import Button from '@material-ui/core/Button'
import LineChart from 'react-linechart';
import '../node_modules/react-linechart/dist/styles.css';
import * as XLSX from 'xlsx'

function App() {
  let [currentTime, setCurrentTime] = useState("N/A");
  let [graph, setGraph]  = useState(false)
  let [graphMessage, setGraphMessage] = useState("Show Graph")
  useEffect(() => {
    const interval = setInterval(() => {fetch('/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    })
  }, 1000);
  return () => clearInterval(interval);
}, []);

  const showGraph = () => {
    setGraphMessage(!graph ? "Unshow Graph" : "Show Graph")
    setGraph(!graph)
  }

  const data = [
    {									
        color: "steelblue", 
        points: [{x: 1, y: 2}, {x: 3, y: 5}, {x: 7, y: -3}] 
    }
]
  
  return (
    <div className="App">
      <header className="App-header">
        <Button style={{color: "white", backgroundColor: "gray"}} onClick={showGraph}>{graphMessage}</Button>
        { !graph ?
            <>
              <img src={logo} className="App-logo" alt="logo" />
              <TestComponent />
              <p> The date is {currentTime}.</p>
              <button onClick={getPred}>Predict</button>
            </>
        :
          <div style={{backgroundColor: "gray", marginTop: "20px"}}>
            <div className="App">
              <h1>My First LineChart</h1>
              <LineChart 
                width={600}
                height={400}
                data={data}
              />
            </div>				
          </div>
      }
      </header>
    </div>
  );
}

function getPred(){

}


export default App;
