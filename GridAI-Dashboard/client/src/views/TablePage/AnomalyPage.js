import React, { Component } from "react";
import StickyHeadTable from "../../components/Table/StickyHeadTable.js";

class AnomalyPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      anomData: [],
      isLoaded: false,
    };
  }

  componentDidMount() {
    this.fetchAnomData();
  }

  fetchAnomData = () => {
    fetch("/allAnom")
      .then((res1) => res1.json())
      .then((data1) =>
        this.setState({
          anomData: data1,
          isLoaded: true,
        })
      );
  };

  render(){

    let {isLoaded, anomData} = this.state;
    if(!isLoaded){
        return(
            <div><h2>Anomaly Data Loading...</h2></div>
        )
    }
    else{

        let anomVal = [];
        for(let i=0;i<anomData["predictions"].length;i++){
            let val = anomData["predictions"][i].split(":");
            anomVal.push({
                "Bus Name": val[0],
                "Status": val[1]
            });
        }

        return(
            <div>
                {
                <StickyHeadTable data={anomVal} />
                }
            </div>
        )

    }
  }
}

export default AnomalyPage;
