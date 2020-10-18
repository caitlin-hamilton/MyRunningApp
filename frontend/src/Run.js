import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Row, Col } from 'reactstrap';

export default class Run extends React.Component{
    constructor(props){
        super(props)
        this.state = {
            id: "", 
            name : "",
            date: "",
            distance: "",
            duration : ""
        }
    }

    componentDidMount() {
        this.setState({
            id: this.props.id, 
            name : this.props.name,
            date: this.removeTimeZone(this.props.date), 
            distance : this.normalizeDistance(this.props.distance),
            duration: this.convertNumToTime(this.props.duration)
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

    render() {
        return (
            <Container>
                <Row>
                    <Col>{this.state.id}</Col>
                    <Col>{this.state.name}</Col>
                    <Col>{this.state.date}</Col>
                    <Col>{this.state.distance}</Col>
                    <Col>{this.state.duration}</Col>
                </Row>
            </Container>
        )
    }
}