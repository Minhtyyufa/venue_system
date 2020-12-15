import React from "react";
import Jumbotron from "react-bootstrap/Jumbotron";
import Container from "react-bootstrap/Container";
import Button from "react-bootstrap/Button";
import { Row} from "react-bootstrap";
import { instanceOf } from "prop-types";
import { withCookies, Cookies } from "react-cookie";
import CustNavBar from "../Helpers/Navbar";


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

  reserveTicket = (ticket_id) => {
    const path = "/venue_system/customer/reserve_ticket/";
  
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
      body: JSON.stringify({ticket_id}),
    })
      .then((res) => {
        return res.json();
      })
      .then(
        (result) => {
          if (Object.keys(result.err).length !== 0 ) {
            alert("Sorry that ticket is now unavailable");
            const urlParams = new URLSearchParams(window.location.search);
            const concert_id = urlParams.get('concert_id');
            this.getTickets(concert_id);
          } else {
            window.location.href="/customer/buy_ticket/?ticket_id=" +ticket_id;
          }
        },
        (error) => {
          //this.setMessage("ERROR sending request", "ERROR");
        }
      );
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
          if (Object.keys(result.err).length !== 0 ) {
            console.log("ERROR");
          } else {
            var tickets = result.msg.payload
            var max_col= Math.max.apply(Math, tickets.map(function(o) { return o.seat_col; }))
            tickets.reshape(max_col, max_col)
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

  
  render() {
    let seats = this.state.tickets.map((value, index) => {

      let seat_row = value.map((val,i) => {
        var style;
        var price;
        if (val.is_available) {
          style="outline-primary";
          price = <p>Price: ${val.price/100}</p>
        } else {
          style="outline-danger";
          price = <p>Unavailable</p>
        }
        return(
        <Button key={val.ticket_id} id={val.ticket_id} variant={style} className="btn-sm" onClick={e => {this.reserveTicket(e.target.id)}}>
          <p>Row: {val.seat_row}, Col: {val.seat_col}</p>
          {price}
        </Button>
        );
      })
      return(<Row key={index}>{seat_row}</Row>);

    });

    return (
      <>
        <CustNavBar />
        <Jumbotron>
          <div style={{ justifyContent: "center", textAlign: "center" }}>
            <h1>Pick a seat and reserve your ticket</h1>
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
