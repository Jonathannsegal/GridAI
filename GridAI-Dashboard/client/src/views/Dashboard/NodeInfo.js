import React, { Component } from "react";
import StickyHeadTable from "../../components/CustomTables/StickyHeadTable.js";
import LineChart from "components/Charts/linechart.js";

class NodeInfo extends Component {
  constructor(props) {
    super(props);
    this.state = {
      info: [],
      lineData: [],
      busname: "",
      input: false,
    };
  }

  componentDidMount() {}

  textChangeHandler = (event) => {
    this.setState({ busname: event.target.value });
    console.log(event.target.value);
  };

  submitHandler = async(event) => {
    event.preventDefault();
    let name = this.state.busname;
    let nodeinfo = await this.fetchNodeinfo(name);
    //Parse nodeinfo for display into table:
    this.parseNodeInfo(nodeinfo);


    let hist = await this.fetchHistory(name);
    let pred = await this.fetchPredictions(name);
    //Parse the history and prediction for linechart:
    this.parseLinedata(name,hist,pred);
  };

  fetchNodeinfo = async (node) => {
    const resp = await fetch(`/busInfo/T_${node}`);
    const data = await resp.json();
    return data;
  };

  fetchHistory = async (node) => {
    const resp = await fetch(`/history/${node}`);
    const data = await resp.json();
    return data;
  };

  fetchPredictions = async (node) => {
    const resp = await fetch(`/allPred`);
    const data = await resp.json();
    for (let i = 0; i < data["predictions"].length; i++) {
      let temp = data["predictions"][i].split(":");
      if ("T_"+node === temp[0]) {
        return data["predictions"][i];
      }
    }
  };

  parseNodeInfo = async (data) =>{
    let temp = [];
    if (data != null) {
      temp.push({
        "Bus Name": data[0]["n"]["BusID"],
        "Current Value": data[0]["n"]["CurrVal"],
        "Previous Value": data[0]["n"]["PrevVal"],
        "Primary voltage rating (kV)": data[0]["n"][`Primary voltage rating (kV)`],
        "Secondary voltage rating (kV)": data[0]["n"]["Secondary voltage rating (kV)"],
        "kVA rating (kVA)": data[0]["n"]["kVA rating (kVA)"],
        "Time": data[0]["n"]["Month"]+" months, " + data[0]["n"]["Day"] + " days, " + data[0]["n"]["Hour"]+ " hours",
      });
    }
    this.setState({ info: temp, input: true });
  }

  parseLinedata = async (name,hist,pred) =>{
    let temparr = [["time", name]];
    let tempdata = [];
    for (let i = 0; i < hist["result"].length; i++) {
      let temp = hist["result"][i].split(" ");
      tempdata = [String(temp[1]), Number(temp[2])];
      temparr.push(tempdata);
    }

    console.log(pred);
    if (pred!= null) {
      let predVal = pred.split(":");
      let temp = ["predicted", Number(predVal[1])];
      temparr.push(temp);
      console.log(temparr[0][1]);
    }
    this.setState({ lineData: temparr });
  }

  render() {
    let { input, info, lineData} = this.state;

    if (input === false) {
      return (
        <div>
          <h4>Please enter a Bus number</h4>
          <form onSubmit={this.submitHandler}>
            <input type="text" name="code" onChange={this.textChangeHandler} />
            <input type="submit" value="Go" />
          </form>
        </div>
      );
    } else {
      return (
        <div>
          <div>
            <h4>Please enter a Bus number</h4>
            <form onSubmit={this.submitHandler}>
              <input
                type="text"
                name="code"
                onChange={this.textChangeHandler}
              />
              <input type="submit" value="Go" />
            </form>
          </div>
          <div>
            <StickyHeadTable data={info} />,
            <LineChart data={lineData} />
          </div>
        </div>
      );
    }
  }
}

export default NodeInfo;
