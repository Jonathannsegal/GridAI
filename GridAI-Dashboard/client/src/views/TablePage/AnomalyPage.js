import React, { Component } from "react";
import { makeStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import StickyHeadTable from "../../components/CustomTables/StickyHeadTable.js";

// const useStyles = {
//   formControl: {
//     margin: theme.spacing(1),
//     minWidth: 120,
//   },
//   selectEmpty: {
//     marginTop: theme.spacing(2),
//   },
// }

class AnomalyPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      anomData: [],
      isLoaded: false,
      filterBy: ''
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
      isLoaded: true
    })
    );
  };
  
  handleChange = (event) => {
    this.setState({
      filterBy: event.target.value
    });
  };
  
  render(){
    let {isLoaded, anomData} = this.state;
    if(!isLoaded){
      return(
        <div><h2>Anomaly Data Loading...</h2></div>
        )
      }
      else{
        
        // const classes = useStyles; className={`${classes.formControl}`}
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
                <FormControl variant="outlined" m={1} style={{ minWidth:150}}>
                      <InputLabel id="demo-simple-select-outlined-label" style={{ minWidth:200 }}>Status</InputLabel>
                      <Select
                        labelId="demo-simple-select-outlined-label"
                        id="demo-simple-select-outlined"
                        value={this.state.filterBy}
                        onChange={this.handleChange}
                        label="Status"
                        style = {{
                          minWidth:150
                        }}
                      >
                        <MenuItem value={'ALL'}></MenuItem>
                        <MenuItem value={'Failure'} style={{ color: 'red'}}>Failure</MenuItem>
                        <MenuItem value={'Spike'} style={{ color: 'orange'}}>Spike</MenuItem>
                        <MenuItem value={'Normal'} style={{ color: 'green'}}>Normal</MenuItem>
                      </Select>
                </FormControl>
                <StickyHeadTable data={anomVal} filterBy={this.state.filterBy} propToFilter={'Status'}/>
            </div>
        )

    }
  }
}

export default AnomalyPage;