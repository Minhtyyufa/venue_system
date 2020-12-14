import React from "react";
import Jumbotron from "react-bootstrap/Jumbotron";
import Container from "react-bootstrap/Container";
import Button from "react-bootstrap/Button";
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import Row from "react-bootstrap/Row";
import Form from "react-bootstrap/Form";
import { Col, Card } from "react-bootstrap";
import { instanceOf } from "prop-types";
import { withCookies, Cookies } from "react-cookie";
import CustNavBar from "../Helpers/Navbar";

class VenueMainPage extends React.Component {
  static propTypes = {
    cookies: instanceOf(Cookies).isRequired,
  };
  constructor(props) {
    super(props);
    this.state = {
      request: {
        concert_name: "",
        artist_id: "",
        date_time: "",
        default_price: "",
      },
      resp_message: {
        message_type: "NONE",
        message: "",
      },
      show_message: false,
      concert_list: [],
    };
    this.getMyConcerts()
  }

  handleChange = (event) => {
    var new_request = this.state.request;
    new_request[event.target.id] = event.target.value;
    this.setState((state) => ({ request: new_request }));
  };

  sendRequest = (event) => {
    event.preventDefault();

    const path = "/venue_system/venue/create_concert/";
  
    const { cookies } = this.props;
    fetch(path, {
      method: "POST",
      headers: {
        "Authorization": "Token " + cookies.get("token"),
        "Cache-Control": "no-cache",
        "Access-Control-Allow-Origin": "http://localhost:8000",
        "Access-Control-Allow-Credentials": true,
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify(this.state.request)
    })
      .then((res) => {
        return res.json();
      })
      .then(
        (result) => {
          console.log(result);
          console.log(Object.keys(result.err).length)
          if (Object.keys(result.err).length != 0 ) {
            console.log("ERROR");
          } else {
            this.setState((state) => ({
              concert_list: result.msg.payload,
            }));
          }
        },
        (error) => {
          //this.setMessage("ERROR sending request", "ERROR");
        }
      );
  };

  getMyConcerts = () =>{
    const path = "/venue_system/venue/get_my_concerts/"
    const { cookies } = this.props;
    fetch(path, {
      method: "GET",
      headers: {
        "Authorization": "Token " + cookies.get("token"),
        "Cache-Control": "no-cache",
        "Access-Control-Allow-Origin": "http://localhost:8000",
        "Access-Control-Allow-Credentials": true,
        "Content-Type": "application/json",
      },
      credentials: "include",
    })
      .then((res) => {
        return res.json();
      })
      .then(
        (result) => {
          console.log(result);
          if (Object.keys(result.err).length != 0 ) {
            console.log("ERROR");
          } else {
            this.setState((state) => ({
              concert_list: result.msg.payload,
            }));
          }
        },
        (error) => {
          //this.setMessage("ERROR sending request", "ERROR");
        }
      );
  }

  render() {
    let concerts = this.state.concert_list.map((value, index) => {
      var date_of_concert = new Date(Date.parse(value.date_time))
      return (

          <Card id= {value.concert_id}className="text-center" style={{ width: '100%' }}>
            <Card.Header>{value.concert_name}</Card.Header>
            <Card.Body>
              <Card.Title>{value.artist_id.band_name}</Card.Title>
              <Card.Text>
                Doors Open: {date_of_concert.getTimezoneOffset()}
              </Card.Text>
              <Card.Text>
                Genre: {value.artist_id.genre}
              </Card.Text>
            </Card.Body>
            <Card.Footer className="text-muted">{date_of_concert.toDateString()}</Card.Footer>
          </Card>
      );
    });

    return (
      <>
        <CustNavBar />

        <Jumbotron>
          <div style={{ justifyContent: "center", textAlign: "center" }}>
            <h1>Welcome to Minh's Venue System, Venue Owner</h1>
            <p>Here you can see your concerts and add more concerts</p>
            <p>
              <Button variant="primary">Learn more</Button>
            </p>
          </div>
        </Jumbotron>
        <Container fluid >
          <Row>
            <Container fluid>
              <Row>
              <h1>Your Tickets</h1>
              </Row>
              <Row style={{ overflowY: "scroll", overflowX: "hidden", maxHeight:1000}}>
                {concerts}
              </Row>
            </Container>
            
          </Row>
          <Row className="h-50">
            <Container fluid>
              <Row>
                <h1>Add Concerts</h1>
              </Row>
              <Row>
                <Col>
                  <Form onSubmit={this.sendRequest}>
                    <Form.Row>
                      <Form.Group controlId="artist_id">
                        <Form.Label>Artist ID</Form.Label>
                        <Form.Control
                          placeholder="43"
                          onChange={this.handleChange}
                        />
                      </Form.Group>
                    </Form.Row>
                    <Form.Row>
                      <Form.Group controlId="concert_name">
                        <Form.Label>Concert Name</Form.Label>
                        <Form.Control
                          placeholder="pop"
                          onChange={this.handleChange}
                        />
                      </Form.Group>
                    </Form.Row>
                    <Form.Row>
                      <Form.Group controlId="date_time">
                        <Form.Label>Date and Time</Form.Label>
                        <Form.Control
                            type="datetime-local"
                          placeholder=""
                          onChange={this.handleChange}
                        />
                      </Form.Group>
                    </Form.Row>
                    <Form.Row>
                      <Form.Group controlId="default_price">
                        <Form.Label>Default Ticket Price</Form.Label>
                        <Form.Control
                            type="number"
                          placeholder=""
                          onChange={this.handleChange}
                        />
                      </Form.Group>
                    </Form.Row>
                    <Button variant="primary" type="submit">
                      Submit
                    </Button>
                  </Form>
                </Col>

        
              </Row>
            </Container>
          </Row>
        </Container>
      </>
    );
  }
}

export default withCookies(VenueMainPage);
