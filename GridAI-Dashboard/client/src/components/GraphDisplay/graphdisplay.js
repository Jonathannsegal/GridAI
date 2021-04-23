import React, { Component } from "react";
import { Graph } from "react-d3-graph";
import LineChart from "../Charts/linechart.js";

const graphstyle = {
  height: "600px",
  width: "1000px",
};

const chartstyle = {
  position: "absolute",
  top: "80px",
  right: "0",
};

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
    labelPosition: "top",
  },
  link: {
    highlightColor: "lightblue",
  },
};

const onClickLink = function (source, target) {
  window.alert(`Clicked link between ${source} and ${target}`);
};

class GraphDisplay extends Component {
  constructor(props) {
    super(props);
    this.state = {
      lineData: [],
      nodeCoords: [],
      multiCheckbox: false,
      isLoaded: false,
    };

    this.onClickNode = this.onClickNode.bind(this);
  }

  componentDidMount() {
    this.fetchNodeCoords();
  }

  fetchNodeCoords = () => {
    fetch("/coordinates")
      .then((res1) => res1.json())
      .then((data1) =>
        this.setState({
          nodeCoords: data1,
          isLoaded: true,
        })
      );
  };

  fetchValue = async (node) => {
    const resp = await fetch(`/allCurrentValues/${node}`);
    const data = await resp.json();
    return data;
  };

  fetchHistory = async (node) => {
    let str = node.split("_");
    const resp = await fetch(`/history/${str[1]}`);
    const data = await resp.json();
    return data;
  };

  fetchPredictions = async (node) => {
    const resp = await fetch(`/allPred`);
    const data = await resp.json();
    for (let i = 0; i < data["predictions"].length; i++) {
      let temp = data["predictions"][i].split(":");
      if (node === temp[0]) {
        return data["predictions"][i];
      }
    }
  };

  onClickNode = async (nodeID) => {
    const val = await this.fetchValue(nodeID);
    if (val[0] == null) {
      window.alert("No value for this node!");
      return;
    }
    window.alert(`Current Value: ${val[0].currentValue}`);

    const hist = await this.fetchHistory(nodeID);
    const pred = await this.fetchPredictions(nodeID);
    if (this.state.multiCheckbox) {
      this.getCompareData(nodeID, hist, pred);
    } else {
      this.getLineData(nodeID, hist, pred);
    }
  };

  getLineData = async (nodeID, hist, pred) => {
    let temparr = [["time", nodeID]];
    let tempdata = [];
    for (let i = 0; i < hist["result"].length; i++) {
      let temp = hist["result"][i].split(" ");
      tempdata = [String(temp[1]), Number(temp[2])];
      temparr.push(tempdata);
    }

    let predVal = pred.split(":");
    let temp = ["predicted", Number(predVal[1])];
    temparr.push(temp);
    console.log(temparr[0][1]);
    this.setState({ lineData: temparr });
  };

  getCompareData = async (nodeID, hist, pred) => {
    var { lineData } = this.state;

    //incase user hasn't first clicked on a node already, don't allow comparision
    if(lineData[0]==null){
      window.alert("Please select a primary node before comparision!");
      return;
    }

    let temparr = [["time", lineData[0][1], nodeID]];
    let tempdata = [];
    for (let i = 0; i < hist["result"].length; i++) {
      let temp = hist["result"][i].split(" ");
      tempdata = [String(temp[1]), lineData[i + 1][1], Number(temp[2])];
      temparr.push(tempdata);
    }

    let predVal = pred.split(":");
    let temp = [
      "predicted",
      lineData[lineData.length - 1][1],
      Number(predVal[1]),
    ];
    temparr.push(temp);
    this.setState({ lineData: temparr });
  };

  onChange = (e) => {
    this.setState({ multiCheckbox: e.target.checked });
  };

  render() {
    if (!this.state.isLoaded) {
      return <div>Loading...</div>;
    } else {
      var { nodeCoords, lineData, multiCheckbox } = this.state;
      let coords = [];
      for (let i = 0; i < nodeCoords.length; i++) {
        coords.push({
          id: nodeCoords[i].BusID,
          x: nodeCoords[i].X * 50 + 100,
          y: nodeCoords[i].Y * -50 + 750,
        });
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
              (console.log("this is linedata"),
              console.log(lineData),
              (<LineChart data={lineData} />))
            }
          </div>
          <div style={graphstyle}>
            {
              <Graph
                id="graph-id" // id is mandatory
                data={{ nodes: coords, links: [] }}
                config={myConfig}
                onClickNode={this.onClickNode}
                onClickLink={onClickLink}
              />
            }
          </div>
          <form>
            <h3>Graph Settings</h3>
            <label>
              Compare nodes?
              <input
                type="checkbox"
                checked={multiCheckbox}
                onChange={this.onChange}
              />
            </label>
          </form>
        </div>
      );
    }
  }
}

export default GraphDisplay;
