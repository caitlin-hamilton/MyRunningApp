import React from 'react';
import axios from "axios";
import './App.css';
import Run from './Run';
import 'bootstrap/dist/css/bootstrap.min.css';
import  { Container, Row, Col, Navbar, SORT_ARROW} from './reactstrap';
import { BiUpArrowAlt, BiDownArrowAlt} from 'react-icons/bi';
import { Nav, NavItem, NavLink, Button } from 'reactstrap';
import {normalizeDistance, removeTimeZone, convertNumToTime, standardiseTime} from './utils';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      runs : [],
      splits: {},
      sortRecord : {
        'date': false,
        'distance': false,
        'duration': false,
      }
    };
    this.sortAttribute = this.sortAttribute.bind(this);
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
sortAttribute(attribute) {
  let runs = [...this.state.runs];
  if (attribute === 'date'){
    if(!this.state.sortRecord[attribute] || this.state.sortRecord[attribute] === 'UP') {
        this.sortDateDescending(runs, attribute)
        this.setState({
          runs,
          sortRecord: this.updateSortRecord(attribute, 'DOWN')
        })
    }
    else if(this.state.sortRecord[attribute] === 'DOWN'){
      this.sortDateAscending(runs, attribute)
        this.setState({
          runs,
          sortRecord: this.updateSortRecord(attribute, 'UP')
        })
    }
  }
  else if (attribute === 'distance'){
    if(!this.state.sortRecord[attribute] || this.state.sortRecord[attribute] === 'UP') {
      this.sortAttrDescending(runs, attribute)
      this.setState({
        runs,
        sortRecord: this.updateSortRecord(attribute, 'DOWN')
      })
  }
  else if(this.state.sortRecord[attribute] === 'DOWN'){
    this.sortAttrAscending(runs, attribute)
      this.setState({
        runs,
        sortRecord: this.updateSortRecord(attribute, 'UP')
      })
    }
  }
  else if(attribute === 'duration'){
    if(!this.state.sortRecord[attribute] || this.state.sortRecord[attribute] === 'UP') {
      this.sortDurationDescending(runs)
      this.setState({
        runs,
        sortRecord: this.updateSortRecord(attribute, 'DOWN')
      })
  }
  else if(this.state.sortRecord[attribute] === 'DOWN'){
    this.sortDurationAscending(runs, attribute)
      this.setState({
        runs,
        sortRecord: this.updateSortRecord(attribute, 'UP')
      })
    }
  }
}

updateSortRecord = (attribute, direction) => {
  let sortRecord = {...this.state.sortRecord}
  Object.keys(sortRecord).forEach(v => sortRecord[v] = false)
  sortRecord[attribute] = direction;
  return sortRecord;
}

sortDateDescending = (runs) => {
  runs.sort(
    (a, b) => new Date(removeTimeZone(a.date)) <= new Date(removeTimeZone(b.date)) ? 1 : -1)
}

sortDateAscending = (runs) => {
  runs.sort(
    (a, b) => new Date(removeTimeZone(a.date)) >= new Date(removeTimeZone(b.date)) ? 1 : -1)
}

sortAttrDescending = (runs, attribute) => {
  runs.sort(
    (a, b) => a[attribute] <= b[attribute] ? 1 : -1)

}
sortAttrAscending = (runs, attribute) => {
  runs.sort(
    (a, b) => a[attribute] >= b[attribute] ? 1 : -1)

}

sortDurationDescending = (runs) => {
  runs.sort(
    (a, b) => new Date(standardiseTime(a.duration)) <= new Date(standardiseTime(b.duration)) ? 1 : -1)
}

sortDurationAscending = (runs) => {
  runs.sort(
    (a, b) => new Date(standardiseTime(a.duration)) >= new Date(standardiseTime(b.duration)) ? 1 : -1)
}

showFastestSplitRun(distance){
  let fastestSplitIds= this.findFastestDistance(distance)
  let runs = this.state.runs;
  for(var i=0; i< runs.length; i++){
    if(fastestSplitIds.includes(runs[i].id)){
      runs[i].showRun = true
    }
    else {
      runs[i].showRun = false
    }
  }
  console.log(fastestSplitIds)
  console.log(runs)
  this.setState({
    runs,
  })
}

findFastestDistance(distance){
  let runs = this.state.runs
  let fastestSplitIds = []
  let fastestTime = 0;

  for(var i=0; i < runs.length;  i++){
    let id = runs[i]['id']
    let splits = runs[i].splits
    let a = splits.filter(split => split['isFastest'])

    for(var j =0; j < a.length; j ++){
      if(fastestSplitIds.length == 0){
        fastestSplitIds.push(id)
        fastestTime = standardiseTime(a[j]['elapsed_time'])
        continue
      }

      if(standardiseTime(a[j]['elapsed_time']) == fastestTime){
        fastestSplitIds.push(id)
        fastestTime = a[j]['elapsed_time']
      }
      else if(standardiseTime(a[j]['elapsed_time']) < fastestTime){
        fastestSplitIds = []
        fastestSplitIds.push(id)
        fastestTime = a[j]['elapsed_time']
      }
    }
  }
 return fastestSplitIds
}





  render() 
    {
      console.log(this.state.runs)
    return (
        <Container fluid="sm">
          <Navbar color="light" light expand="md">
            <Nav>
              <NavItem>
                <Button onClick={() => this.sortAttribute('date')} color="light"> Date { SORT_ARROW[this.state.sortRecord['date']] }  </Button>
              </NavItem>
              <NavItem>
                <Button onClick={() => this.sortAttribute('distance')} color="light"> Distance { SORT_ARROW[this.state.sortRecord['distance']] }  </Button>
              </NavItem>
              <NavItem>
                <Button onClick={() => this.sortAttribute('duration')} color="light"> Time { SORT_ARROW[this.state.sortRecord['duration']] }  </Button>
              </NavItem>
            </Nav>
          </Navbar>
              {this.state.runs.map(item => <Run id={item.id} duration={item.duration} date={item.date} name={item.name} distance={item.distance} key={item.id} splits={this.getSplitsById(item.id)}/>)}
        </Container>
    )
  }
}


export default App;
