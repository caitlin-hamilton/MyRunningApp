import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import  { Container, Row, Col } from './reactstrap';
import { BiMedal } from 'react-icons/bi';

export default class Split extends React.Component {
        constructor(props){
        super(props)
        this.state = {
            isFastest: false,
            id: "", 
            split_number : "",
            elapsed_time: "",
            moving_time: "",
        }
    }

    componentDidMount(){
        this.setState(
            {
                isFastest: this.props.isFastest,
                id: this.props.key, 
                split_number : this.props.split_number,
                elapsed_time: this.props.elapsed_time,
                moving_time: this.props.moving_time,
            }
        )

    }
    render(){
        return(
            <div>
                <Container style={{backgroundColor: '#f1f1f1'}}>
                <Row>
                    <Col >{this.state.isFastest === true? <BiMedal size={18} className="float-right align-bottom"/> : ""}</Col>
                    <Col style={{"borderTop": '1px solid light-grey'}}>{this.state.split_number}</Col>
                    <Col>{this.state.elapsed_time}</Col>
                    <Col>{this.state.moving_time}</Col>
                </Row>
            </Container>
            </div>
        )
    }
}