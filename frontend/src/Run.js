import React from 'react';
import { Container, Row, Col } from 'reactstrap';
import PropTypes from 'prop-types'
import 'bootstrap/dist/css/bootstrap.min.css';

Container.propTypes = {
    fluid: PropTypes.oneOfType([PropTypes.bool, PropTypes.string])
    // applies .container-fluid class if bool or .container-{breakpoint} if string
  }

  Row.propTypes = {
    noGutters: PropTypes.bool,
    // see https://reactstrap.github.io/components/form Form Grid with Form Row
    form: PropTypes.bool,
    xs: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    sm: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    md: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    lg: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    xl: PropTypes.oneOfType([PropTypes.number, PropTypes.string])
  }

  const stringOrNumberProp = PropTypes.oneOfType([PropTypes.number, PropTypes.string]);
const columnProps = PropTypes.oneOfType([
  PropTypes.string,
  PropTypes.number,
  PropTypes.bool,
  PropTypes.shape({
    size: PropTypes.oneOfType([PropTypes.bool, PropTypes.number, PropTypes.string]),
    // example size values:
    // 12 || "12" => col-12 or col-`width`-12
    // auto => col-auto or col-`width`-auto
    // true => col or col-`width`
    order: stringOrNumberProp,
    offset: stringOrNumberProp
  })
]);

Col.propTypes = {
  xs: columnProps,
  sm: columnProps,
  md: columnProps,
  lg: columnProps,
  xl: columnProps,
  widths: PropTypes.array,
}

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