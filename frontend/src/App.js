import React from 'react';
import axios from "axios";
import './App.css';
import Run from './Run';

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
    this.getSplits();
  }

  renderRuns = async() => {
  try {
    let res = await axios.get("http://localhost:8000/my_runs/");
    let data = res.data;
    console.log(data)
    let runs = [...this.state.runs]
    runs = runs.concat(data)
    this.setState({
      runs: runs
    });
  } catch (err) {
    console.log(err);
  }
}

getSplits = async() => {
  let runs = this.state.runs
  try {
    for(var i=0; i < runs.length- 1; i ++){
      let activity_id = runs.id
      let res = await axios.get()
    }
    
  }
  catch (err){
    console.log(err)
  }
}

  render() 
    {
    return (
      <div>
            {this.state.runs.map((item, index) => <Run id={item.id} duration={item.duration} date={item.date} name={item.name} distance={item.distance} key={item.id}/>)}
      </div>
    )
  }
}


export default App;
