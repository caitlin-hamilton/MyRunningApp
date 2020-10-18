import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Row, Col } from 'reactstrap';
import Split from './Split';

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
            date: this.removeTimeZone(this.props.date), 
            distance : this.normalizeDistance(this.props.distance),
            duration: this.convertNumToTime(this.props.duration),
            splits: this.props.splits
        })
      }

    normalizeDistance(distance){
        distance = distance/1000
        return distance.toFixed(2)
    }

    removeTimeZone(date){
        date = date.split("T")[0]
        return date
    }

    convertNumToTime(number) {
        var myDate = new Date(number *1000);
        var gmtDate = new Date(myDate.toGMTString())
        return gmtDate.getUTCHours() + ":" + gmtDate.getUTCMinutes() +":" + gmtDate.getUTCSeconds()
    }

    toggleSplits() {
        let toggleValue = true ? this.state.showSplits === false : false
        this.setState({
            showSplits: toggleValue
        })
    }

    render() {
        console.log(this.state)
        return (
            <Container>
                <Row>
                    <Col onClick={() => this.toggleSplits()}>{this.state.id}</Col>
                    <Col>{this.state.name}</Col>
                    <Col>{this.state.date}</Col>
                    <Col>{this.state.distance}</Col>
                    <Col>{this.state.duration}</Col>
                </Row>
                <div>
                    {this.state.showSplits && this.state.splits.map((item) => <Split split_number={item['split_number']} elapsed_time={this.convertNumToTime(item['elapsed_time'])} moving_time={this.convertNumToTime(item['moving_time'])} avg_pace={this.convertNumToTime(item['avg_pace'])}/>)}
                </div>
            </Container>
        )
    }
}