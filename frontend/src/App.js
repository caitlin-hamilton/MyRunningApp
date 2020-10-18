import React from 'react';
import axios from "axios";
import './App.css';
import Run from './Run';
import Split from './Split';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      runs : [],
      splits: {}
    };
  }

  componentDidMount() {
    this.renderRuns();
  }

  renderRuns = async() => {
  try {
    let res = await axios.get("http://localhost:8000/my_runs/runs");
    let data = res.data;
    let runs = [...this.state.runs]
    runs = runs.concat(data)
    let splits = this.getSplits(runs)
    this.setState({
      runs,
      splits
    });

    this.getSplits(runs)
    
  } catch (err) {
    console.log(err);
  }
}

getSplits = (runs)  => {
  let splits = {}
  for (const [key, value] of Object.entries(runs)){
    splits[value["id"]]  = value['splits']
  }
  return splits
}

renderSplits = (run_id) => {
  let run_splits = this.state.splits[run_id]
  let arr = []
  for(var i=0; i< run_splits.length -1; i++){
    arr.push(<Split split_number={run_splits[i]['split_number']} elapsed_time={run_splits[i]['elapsed_time']} moving_time={run_splits[i]['moving_time']} avg_pace={run_splits[i]['avg_pace']}   />)
  }
  console.log(arr)
  return arr
}

renderRunAndSplits = () => {
  let arr = []
  let runs = this.state.runs;
  
}

  render() 
    {
    return (
      <div>
            {this.state.runs.map(item => <Run id={item.id} duration={item.duration} date={item.date} name={item.name} distance={item.distance} key={item.id}/>)}
            {this.state.runs.map(run => {return this.renderSplits(run.id).map(split => split)})}
      </div>

    )
  }
}


export default App;
