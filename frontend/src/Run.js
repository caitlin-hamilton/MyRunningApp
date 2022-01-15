import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import  { Container, Row, Col } from './reactstrap';
import Split from './Split';
import { BiRun } from 'react-icons/bi';
import {normalizeDistance, removeTimeZone, convertNumToTime} from './utils';


export default class Run extends React.Component{
    constructor(props){
        super(props)
        this.state = {
            id: "", 
            name : "",
            date: "",
            distance: "",
            duration : "",
            splits : [],
            showSplits: false
        }
        this.toggleSplits = this.toggleSplits.bind(this);
        this.findFastestSplit = this.findFastestSplit.bind(this);
        this.formatSplits = this.formatSplits.bind(this);
        
    }

    componentDidMount() {
        this.setState({
            id: this.props.id, 
            name : this.props.name,
            date: removeTimeZone(this.props.date), 
            distance : normalizeDistance(this.props.distance),
            duration: convertNumToTime(this.props.duration),
            splits: this.formatSplits(normalizeDistance(this.props.distance),this.props.splits),
        })
      }

    toggleSplits() {
        let toggleValue = true ? this.state.showSplits === false : false
        this.setState({
            showSplits: toggleValue
        })
    }

    findFastestSplit(distance, splits) {
        if(splits.length ===1){
            return [1]
        }
        let sorted_splits = [...splits].sort(function(a,b) { return a.elapsed_time - b.elapsed_time;})
//        if(!this.checkIfSplitIsOneKm(distance)){
//            sorted_splits.shift()
//        }
        let fastest_splits = this.checkIfTimeDuplicated(sorted_splits)
        return fastest_splits
    }

    checkIfSplitIsOneKm(distance) {
        if(distance % 1 === 0){
            return true
        }
        return false
    }

    checkIfTimeDuplicated(splits){
        let fastest_time = splits[0]['elapsed_time']
        let dup_number = splits.filter((v) => (parseFloat(v['elapsed_time']) === parseFloat(fastest_time))).length;
        let fastest_splits = splits.slice(0, dup_number).map(item => item['split_number'])
        return fastest_splits
    }

    formatSplits(distance,splits){
        let fastest_splits = this.findFastestSplit(distance, splits)
        splits.forEach((item) => item['isFastest'] = fastest_splits.includes(item['split_number']) ? true: false)
        return splits
    }


    render() {
        return (
            <div>
            <Container width="50%" style={{backgroundColor: '#f1f1f1'}} className='mt-3'>
                { <Row  onClick={() => this.toggleSplits()}>
                    <Col> <BiRun size={32}/> {this.state.name}</Col>
                </Row> }
                <Row onClick={() => this.toggleSplits()} style={{"borderTop": '1px solid black'}}>
                    <Col >{this.state.id}</Col>
                    <Col>{this.state.date}</Col>
                    <Col >{this.state.distance} km</Col>
                    <Col>{this.state.duration}</Col>
                </Row>
                <Row onClick={() => this.toggleSplits()}>
                    <Col></Col>
                    <Col>Date</Col>
                    <Col>Distance</Col>
                    <Col>Time</Col>
                </Row> 
                { this.state.showSplits && 
                <Row style={{"borderTop": '1px solid black'}}>
                    <Col></Col>
                    <Col>Split 1km</Col>
                    <Col>Elapsed time (Mins)</Col>
                    <Col>Moving time (Mins)</Col>
                </Row>
                }
            </Container>
            {this.state.showSplits && this.state.splits.map((item) => <Split key={item['split_number']}isFastest={item['isFastest']} split_number={item['split_number']} elapsed_time={item['elapsed_time']} moving_time={item['moving_time']}/>)}
            </div>
        )
    }
}