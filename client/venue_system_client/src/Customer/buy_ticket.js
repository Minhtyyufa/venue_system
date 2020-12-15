import React from "react";
import Container from "react-bootstrap/Container";
import Button from "react-bootstrap/Button";
import Row from "react-bootstrap/Row";
import Form from "react-bootstrap/Form";
import { Col } from "react-bootstrap";
import { instanceOf } from "prop-types";
import { withCookies, Cookies } from "react-cookie";
import Timer from "react-compound-timer";
import CustNavBar from "../Helpers/Navbar";


class BuyTicketPage extends React.Component {
  static propTypes = {
    cookies: instanceOf(Cookies).isRequired,
  };
  constructor(props) {
    super(props);
    const urlParams = new URLSearchParams(window.location.search);
    const ticket_id = urlParams.get("ticket_id");
    this.state = {
      request: {
        credit_card: {
          new: true,
          credit_card_number: "",
          security_code: 0,
          expiration_date: 0,
          card_nickname: "",
          credit_card_id: "",
        },
        ticket_id: ticket_id,
      },
      month: 0,
      year: 0,
      resp_message: {
        message_type: "NONE",
        message: "",
      },
    };
  }

  handleChange = (event) => {
    var new_request = this.state.request;
    if (event.target.id === "new") {
      new_request["credit_card"][event.target.id] = event.target.checked;
    } else if (event.target.id === "month") {
      new_request["credit_card"]["expiration_date"] =
        100 * parseInt(event.target.value) + this.state.year;
      this.setState((state) => ({
        month: parseInt(event.target.value),
      }));
    } else if (event.target.id === "year") {
      new_request["credit_card"]["expiration_date"] =
        100 * this.state.month + parseInt(event.target.value);
      this.setState((state) => ({
        year: parseInt(event.target.value),
      }));
    } else {
      new_request["credit_card"][event.target.id] = event.target.value;
    }

    this.setState((state) => ({ request: new_request }));
  };

  sendRequest = (event) => {
    event.preventDefault();

    const path = "/venue_system/customer/confirm_ticket/";
    const { cookies } = this.props;
    fetch(path, {
      method: "POST",
      headers: {
        Authorization: "Token " + cookies.get("token"),
        "Cache-Control": "no-cache",
        "Access-Control-Allow-Origin": "http://localhost:8000",
        "Access-Control-Allow-Credentials": true,
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify(this.state.request),
    })
      .then((res) => {
        return res.json();
      })
      .then(
        (result) => {
          if (Object.keys(result.err).length !== 0) {
            console.log("ERROR");
          } else {
            alert("Successfully bought the ticket");
          }
        },
        (error) => {
          //this.setMessage("ERROR sending request", "ERROR");
        }
      );
  };

  render() {
    let new_card_form = (
      <>
        <Form.Row>
          <Form.Group controlId="card_nickname">
            <Form.Label>Card Nickname</Form.Label>
            <Form.Control
              placeholder="Card Nickname"
              onChange={this.handleChange}
            />
          </Form.Group>
        </Form.Row>
        <Form.Row>
          <Form.Group controlId="credit_card_number">
            <Form.Label>Credit Card Number</Form.Label>
            <Form.Control
              placeholder="1234 5678 9012 3456"
              onChange={this.handleChange}
            />
          </Form.Group>
        </Form.Row>
        <Form.Row>
          <Form.Group controlId="security_code">
            <Form.Label>Security_code</Form.Label>
            <Form.Control
              placeholder={123}
              type="number"
              onChange={this.handleChange}
            />
          </Form.Group>
        </Form.Row>

        <Form.Row>
          <Form.Group>
            <Form.Label>Expiration Date</Form.Label>
            <Form.Row>
              <Col>
                <Form.Control
                  id="month"
                  placeholder="Month"
                  type="number"
                  onChange={this.handleChange}
                />
              </Col>
              <Col>
                <Form.Control
                  id="year"
                  placeholder="Year (ex. 20)"
                  type="number"
                  onChange={this.handleChange}
                />
              </Col>
            </Form.Row>
          </Form.Group>
        </Form.Row>
      </>
    );

    let reuse_card_form = (
      <Form.Row>
        <Form.Group controlId="credit_card_id">
          <Form.Label>Credit Card ID</Form.Label>
          <Form.Control
            placeholder="Credit Card ID"
            onChange={this.handleChange}
          />
        </Form.Group>
      </Form.Row>
    );
    
    var form;
    if (this.state.request.credit_card.new) {
      form = new_card_form;
    } else form = reuse_card_form;

    return (
      <>
        <CustNavBar/>

        <Container fluid>
          <Row>
            <h1>Billing Information</h1>
          </Row>
          <Row>
            <Timer initialTime={60000 * 5} direction="backward">
              {() => (
                <React.Fragment>
                  <h2>
                    Time left to purchase ticket:     <Timer.Minutes /> :{" "}
                    <Timer.Seconds />
                  </h2>
                </React.Fragment>
              )}
            </Timer>
          </Row>
          <Row>
            <Col>
              <Form onSubmit={this.sendRequest}>
                <Form.Row>
                  <Form.Group controlId="new" id="new">
                    <Form.Label>New Credit Card</Form.Label>
                    <Form.Check
                      defaultChecked={true}
                      placeholder=""
                      onChange={this.handleChange}
                    />
                  </Form.Group>
                </Form.Row>
                {form}
                <Button variant="primary" type="submit">
                  Submit
                </Button>
              </Form>
            </Col>
          </Row>
        </Container>
      </>
    );
  }
}

export default withCookies(BuyTicketPage);
