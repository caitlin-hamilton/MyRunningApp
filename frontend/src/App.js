import React from 'react';
import axios from "axios";
import './App.css';
import Run from './Run';
import 'bootstrap/dist/css/bootstrap.min.css';
import  { Container, Row, Col } from './reactstrap';

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

getSplitsById = (run_id) => {
  let run_splits = this.state.splits[run_id]
  return run_splits
}

  render() 
    {
    return (
      <div>
            {this.state.runs.map(item => <Run id={item.id} duration={item.duration} date={item.date} name={item.name} distance={item.distance} key={item.id} splits={this.getSplitsById(item.id)}/>)}
      </div>

    )
  }
}


export default App;
