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

class CustomerMainPage extends React.Component {
  static propTypes = {
    cookies: instanceOf(Cookies).isRequired,
  };
  constructor(props) {
    super(props);
    var d = new Date();
    this.state = {
      request: {
        artist_id__band_name: "",
        artist_id__genre: "",
        venue_id__venue_name: "",
      },
      resp_message: {
        message_type: "NONE",
        message: "",
      },
      show_message: false,
      concert_list: [],
    };
  }

  handleChange = (event) => {
    var new_request = this.state.request;
    new_request[event.target.id] = event.target.value;
    this.setState((state) => ({ request: new_request }));
  };

  sendRequest = (event) => {
    event.preventDefault();

    const path = "/venue_system/customer/find_concerts/";
    //var url = new URL(path);
    var query_params = new URLSearchParams(this.state.request).toString();
    const { cookies } = this.props;
    fetch(path + "?" + query_params, {
      method: "GET",
      headers: {
        Authorization: "Token " + cookies.get("token"),
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

  render() {
    let concerts = this.state.concert_list.map((value, index) => {
      var date_of_concert = new Date(Date.parse(value.date_time))
      return (
        <Row key = {value.concert_id} id= {value.concert_id}>
          <Card className="text-center" style={{ width: '100%' }}>
            <Card.Header>{value.concert_name}</Card.Header>
            <Card.Body>
              <Card.Title>{value.artist_id.band_name} at {value.venue_id.venue_name}</Card.Title>

              <Card.Text>
                Address: {value.venue_id.address}
              </Card.Text>
              <Card.Text>
                Doors Open: {date_of_concert.getTimezoneOffset()}
              </Card.Text>
              <Card.Text>
                Genre: {value.artist_id.genre}
              </Card.Text>
              <Button variant="primary" href={"/customer/view_tickets/?concert_id=" + value.concert_id}>Buy Tickets</Button>
            </Card.Body>
            <Card.Footer className="text-muted">{date_of_concert.toDateString()}</Card.Footer>
          </Card>
        </Row>
      );
    });

    return (
      <>
        <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
          <Navbar.Brand href="/about">Venue System</Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="mr-auto">
              <Nav.Link href="#features">Features</Nav.Link>
              <Nav.Link href="#pricing">Pricing</Nav.Link>
            </Nav>
            <Nav>
              <Nav.Link href="#deets">Logout</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Navbar>

        <Jumbotron>
          <div style={{ justifyContent: "center", textAlign: "center" }}>
            <h1>Welcome to Minh's Venue System</h1>
            <p>Here you can see your tickets and search for concerts</p>
            <p>
              <Button variant="primary">Learn more</Button>
            </p>
          </div>
        </Jumbotron>
        <Container fluid >
          <Row>
            <h1>Your Tickets</h1>
          </Row>
          <Row className="h-50">
            <Container fluid>
              <Row>
                <h1>Search For Concerts</h1>
              </Row>
              <Row>
                <Col>
                  <Form onSubmit={this.sendRequest}>
                    <Form.Row>
                      <Form.Group controlId="artist_id__band_name">
                        <Form.Label>Band Name</Form.Label>
                        <Form.Control
                          placeholder="The Strokes"
                          onChange={this.handleChange}
                        />
                      </Form.Group>
                    </Form.Row>
                    <Form.Row>
                      <Form.Group controlId="artist_id__genre">
                        <Form.Label>Genre</Form.Label>
                        <Form.Control
                          placeholder="pop"
                          onChange={this.handleChange}
                        />
                      </Form.Group>
                    </Form.Row>
                    <Form.Row>
                      <Form.Group controlId="venue_id__venue_name">
                        <Form.Label>Venue Name</Form.Label>
                        <Form.Control
                          placeholder="Bowery Ballroom"
                          onChange={this.handleChange}
                        />
                      </Form.Group>
                    </Form.Row>

                    <Button variant="primary" type="submit">
                      Submit
                    </Button>
                  </Form>
                </Col>

                <Col style={{maxHeight: 1000}}>
                  <div
                    style={{ overflowY: "scroll", overflowX: "hidden" }}
                    className="h-50"
                  >
                    {concerts}
                  </div>
                </Col>
              </Row>
            </Container>
          </Row>
        </Container>
      </>
    );
  }
}

export default withCookies(CustomerMainPage);
