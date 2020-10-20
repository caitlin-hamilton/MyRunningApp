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
        this.toggleSplits = this.toggleSplits.bind(this)
    }

    componentDidMount() {
        this.setState({
            id: this.props.id, 
            name : this.props.name,
            date: removeTimeZone(this.props.date), 
            distance : normalizeDistance(this.props.distance),
            duration: convertNumToTime(this.props.duration),
            splits: this.props.splits
        })
      }

    toggleSplits() {
        let toggleValue = true ? this.state.showSplits === false : false
        this.setState({
            showSplits: toggleValue
        })
    }

    render() {
        return (
            <Container style={{backgroundColor: '#f1f1f1', border: '10px solid white'}}>
                <Row onClick={() => this.toggleSplits()}>
                    <Col>{this.state.name} <BiRun size={32}/></Col>
                </Row>
                <Row onClick={() => this.toggleSplits()} style={{"border-top": '1px solid black'}}>
                    <Col>{this.state.date}</Col>
                    <Col>{this.state.distance} km</Col>
                    <Col>{this.state.duration}</Col>
                </Row>
                <Row onClick={() => this.toggleSplits()}>
                    <Col>Date</Col>
                    <Col>Distance</Col>
                    <Col>Time</Col>
              </Row>
                { this.state.showSplits && 
                <Row style={{"border-top": '1px solid black'}}>
                    <Col></Col>
                    <Col>Split 1km</Col>
                    <Col>Elapsed time</Col>
                    <Col>Moving time</Col>
                    <Col>Avg pace</Col>
                </Row>
                }
                    {this.state.showSplits && this.state.splits.map((item) => <Split split_number={item['split_number']} elapsed_time={convertNumToTime(item['elapsed_time'])} moving_time={convertNumToTime(item['moving_time'])} avg_pace={this.convertNumToTime(item['avg_pace'])}/>)}
            </Container>
        )
    }
}