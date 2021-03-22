import React, { Component } from 'react';
import { Graph } from "react-d3-graph"



  // the graph configuration, just override the ones you need
  const myConfig = {
    height: 800,
    width: 750,
    staticGraph: true,
    staticGraphWithDragAndDrop: false,
    nodeHighlightBehavior: true,
    node: {
      color: "lightgreen",
      size: 120,
      highlightStrokeColor: "blue",
      labelPosition:"top"
    },
    link: {
      highlightColor: "lightblue",
    },
  };

  const onClickNode = function(nodeId) {
    window.alert(`Clicked node ${nodeId}`);
  };

  const onClickLink = function(source, target) {
    window.alert(`Clicked link between ${source} and ${target}`);
  };

  //const topContainer = useRef();

class GraphDisplay extends Component{

  constructor(props) {
    super(props);
    this.state = {
      coords:[],
      isLoaded: false,
    }
  }

  // componentDidMount() {

  //   Promise.all([

  //   fetch('/coords'),
  //   fetch('/lineA')])
  //   .then(([res1, res2]) => Promise.all([res1.json(),res2.json()]))
  //   .then(([data1, data2]) => this.setState({

  //     coords:data1, lineA:data2, isLoaded:true
  //   }))

    
  // }

  componentDidMount() {
    this.fetchCoords();
  }

  fetchCoords = () => {
    fetch('/coordinates').then(res1 => res1.json()).then((data1) => this.setState({
    coords:data1,
    isLoaded:true
    }));
  }
  

  render(){


    if(!this.state.isLoaded){
      return <div>Loading...</div>;
    }

    else{

      var {coords} = this.state;
      let data = [];
      for(let i=0;i<coords.length;i++){
        data.push({id: coords[i].BusID, x:coords[i].X*50+100, y:coords[i].Y*-50+750})
      }

      // let link = [];
      // for(let i=0;i<alldata[1].length;i++){
      //   link.push({source: "bus"+String(alldata[1][i].n.BusA), target:"bus"+String(alldata[1][i].n.BusB)})
      // }
      // for(let i=0;i<alldata[2].length;i++){
      //   link.push({source: "bus"+String(alldata[2][i].n.BusA), target:"bus"+String(alldata[2][i].n.BusB)})
      // }
      // for(let i=0;i<alldata[3].length;i++){
      //   link.push({source: "bus"+String(alldata[3][i].n.BusA), target:"bus"+String(alldata[3][i].n.BusB)})
      // }

      return (
        <div className="App">
        {
          <Graph 
      id="graph-id" // id is mandatory
      data={{nodes:data}}
      config={myConfig}
      onClickNode={onClickNode}
      onClickLink={onClickLink}
      /> }
      </div>
      );
    } 

  }
}


export default GraphDisplay;