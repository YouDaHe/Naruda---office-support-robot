// 맵, 버튼, 태스크

import React, { Component } from 'react'
import { observer } from 'mobx-react'
import { Form } from 'semantic-ui-react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import styled from 'styled-components'
import { Container } from 'semantic-ui-react'
import 'semantic-ui-less/semantic.less'

const Wrapper = styled.div`
    width: ${props => props.width};
    height: ${props => props.height};
`;

@observer
export default class Body extends Component {
  constructor(props) {
    super(props);
    this.state = {
      xcoord: '', ycoord: '',
      narumiXcoord: 0, narumiYcoord: 0
    }
  }

  componentDidMount() {
    this.map = L.map('map', {
      center: [58, 16],
      zoom: 6,
      zommControl: false
    });
    L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png').addTo(this.map);

    this.props.updatePos()
      .then(res => {
        this.setState(state => ({ ...state, narumiXcoord: res.xcoord, narumiYcoord: res.ycoord }))
      })
      
    this.props.updateTask()
  }

  componentWillUnmount() {
  }

  handleChange = (e, { name, value }) => {
    this.setState({ [name]: parseInt(value, 10) })
  }

  handleSubmit = (e) => {
    e.preventDefault();
    this.props.addTask(this.state.xcoord, this.state.ycoord);
  }

  render() {
    const { xcoord, ycoord, narumiXcoord, narumiYcoord } = this.state
    return (
      <div>
        <Container textAlign='center'>
          <Wrapper width="1000px" height="720px" id="map" />
        </Container>
        <Form onSubmit={this.handleSubmit}>
          <Form.Group>
            <Form.Input label='X Coordinate' name='xcoord' placeholder='X Coordinate' value={this.state.xcoord} onChange={this.handleChange}></Form.Input>
            <Form.Input label='Y Coordinate' name='ycoord' placeholder='Y Coordinate' value={this.state.ycoord} onChange={this.handleChange}></Form.Input>
            <Form.Button type='submit'>Call Narumi</Form.Button>
          </Form.Group>
        </Form>
        {/* to be removed */}
        <strong>onChange:</strong>
        <pre>{JSON.stringify({ xcoord, ycoord, narumiXcoord, narumiYcoord }, null, 4)}</pre>
      </div>
    );
  }
}