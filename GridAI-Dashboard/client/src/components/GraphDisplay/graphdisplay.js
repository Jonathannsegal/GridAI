import React, { Component, useState } from 'react';
import { Graph } from "react-d3-graph"
import StickyHeadTable from "../Table/StickyHeadTable.js"
import LineChart from "../Charts/linechart.js"

  // the graph configuration, just override the ones you need

  //var lineData = [['x','kWh'],['T_2040',4.56]];

  const graphstyle = {
    height: "600px",
    width: "1000px"
  }

  const chartstyle = {
    position: "absolute",
    top: "80px",
    right: "0"
  }

  const myConfig = {
    height: 600,
    width: 1000,
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

  const onClickLink = function(source, target) {
    window.alert(`Clicked link between ${source} and ${target}`);
  };

class GraphDisplay extends Component{

  constructor(props) {
    super(props);
    this.state = {
      lineData:[['x','kWh']],
      nodeData:[],
      isLoaded: false,
    }

    this.onClickNode = this.onClickNode.bind(this)
  }

  componentDidMount() {
    this.fetchNodeData();
  }

  fetchNodeData = () =>{
    fetch('/alldata').then(res1 => res1.json()).then((data1) => this.setState({
      nodeData:data1,
      isLoaded:true
      }));
  }

  fetchValue = async(node) => {
    const resp = await fetch(`/CurrentValues/${node}`);
    const data = await resp.json();
    return data;
  }

  onClickNode = async(nodeID)=>{
    const val = await this.fetchValue(nodeID);
    console.log(val[0]);
    window.alert(`Current Value: ${val[0].currentval}`);
    let tempdata = [nodeID,val[0].currentval]
    let temparr = this.state.lineData;
    temparr.push((tempdata))
    console.log("this is tempArr in function")
    console.log(temparr)
    this.setState({lineData:temparr})
  };

  render(){
    
    console.log(this.state.nodeData)
    if(!this.state.isLoaded){
      return <div>Loading...</div>;
    }

    else{

      var {nodeData,lineData} = this.state;
      let data = [];
      for(let i=0;i<nodeData[0].length;i++){
        data.push({id: nodeData[0][i].BusID, x:nodeData[0][i].X*50+100, y:nodeData[0][i].Y*-50+750})
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
      <div>
        <div style={chartstyle}>
          {
          console.log("this is lineData in render"),
          console.log(lineData),
          <LineChart data={lineData}/>
        }
        </div>
        <div style={graphstyle}>
        {
          <Graph
          id="graph-id" // id is mandatory
          data={{nodes:data,links:[]}}
          config={myConfig}
          onClickNode={this.onClickNode}
          onClickLink={onClickLink}
          /> 
        }
        </div>

    </div>
      );
    } 

  }
}


export default GraphDisplay;