import React from "react";
import Jumbotron from "react-bootstrap/Jumbotron";
import Container from "react-bootstrap/Container";
import Button from "react-bootstrap/Button";
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import { Col, Card, Row} from "react-bootstrap";
import { instanceOf } from "prop-types";
import { withCookies, Cookies } from "react-cookie";
Array.prototype.reshape = function(rows, cols) {
  var copy = this.slice(0); // Copy all elements.
  this.length = 0; // Clear out existing array.

  for (var r = 0; r < rows; r++) {
    var row = [];
    for (var c = 0; c < cols; c++) {
      var i = r * cols + c;
      if (i < copy.length) {
        row.push(copy[i]);
      }
    }
    this.push(row);
  }
};

class ReserveTicketPage extends React.Component {
  static propTypes = {
    cookies: instanceOf(Cookies).isRequired,
  };
  constructor(props) {
    super(props);
    var d = new Date();
    const urlParams = new URLSearchParams(window.location.search);
    const concert_id = urlParams.get('concert_id');
    
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
      tickets: [],
    };
    this.getTickets(concert_id);
  }

  getTickets = (concert_id) => {
    const path = "/venue_system/customer/get_tickets_by_concert_id/";
    var query_params = new URLSearchParams({concert_id}).toString();
    const { cookies } = this.props;
    fetch(path + "?" + query_params, {
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
          console.log(Object.keys(result.err).length)
          if (Object.keys(result.err).length != 0 ) {
            console.log("ERROR");
          } else {
            var tickets = result.msg.payload
            var max_col= Math.max.apply(Math, tickets.map(function(o) { return o.seat_col; }))
            tickets.reshape(max_col, max_col)
            console.log(tickets);
            this.setState((state) => ({
              tickets: tickets,
            }));
          }
        },
        (error) => {
          //this.setMessage("ERROR sending request", "ERROR");
        }
      );
  };
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
    let seats = this.state.tickets.map((value, index) => {

      let seat_row = value.map((val,i) => {
        if (val.is_available) {
          var style="outline-primary";
          var price = <p>Price: ${val.price/100}</p>
        } else {
          var style="outline-danger";
          var price = <p>Unavailable</p>
        }
        return(
        <Button key={val.ticket_id} id={val.ticket_id} variant={style} className="btn-sm">
          <p>Row: {val.seat_row}, Col: {val.seat_col}</p>
          {price}
        </Button>
        );
      })
      return(<Row key={index}>{seat_row}</Row>);

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
          {seats}
        </Container>
      </>
    );
  }
}

export default withCookies(ReserveTicketPage);
