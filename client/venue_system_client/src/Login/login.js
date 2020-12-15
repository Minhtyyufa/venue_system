import React from "react";
import { Navbar, Form, Button, Container } from "react-bootstrap";
import fetch from "fetch-with-proxy";
import { instanceOf } from "prop-types";
import { withCookies, Cookies } from "react-cookie";

class LoginPage extends React.Component {
  static propTypes = {
    cookies: instanceOf(Cookies).isRequired,
  };
  constructor(props) {
    super(props);
    this.state = {
      request: {
        username: "",
        password: "",
      },
      resp_message: {
        message_type: "NONE",
        message: "",
      },
      show_message: false,
    };
  }

  handleChange = (event) => {
    var new_request = this.state.request;
    new_request[event.target.id] = event.target.value;
    this.setState((state) => ({ request: new_request }));
  };

  sendRequest = (event) => {
    event.preventDefault();
    const path = "/venue_system/api-token-auth/";

    fetch(path, {
      method: "POST",
      headers: {
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
          if (result.token !== null && result.token !== undefined) {
            const { cookies } = this.props;
            cookies.set("token", result["token"], { path: "/" });
            this.redirect(event);
          } else {
            //this.setMessage("Successfully Logged in", "SUCCESS");
          }
        },
        (error) => {
          //this.setMessage("ERROR sending request", "ERROR");
        }
      );
  };

  redirect = (event) => {
    const { cookies } = this.props;

    const path = "/venue_system/admin/get_user_type/";
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
          if (Object.keys(result.err).length !== 0) {
            console.log("ERROR");
          } else {
            if (result.msg.payload === 2) {
              window.location.href = "/";
            } else if (result.msg.payload === 1) {
              window.location.href = "/venue_owner";
            } else {
              alert("Sorry Artists haven't been added yet :(");
            }
          }
        },
        (error) => {
          //this.setMessage("ERROR sending request", "ERROR");
        }
      );
  };
  render() {
    return (
      <>
        <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
          <Navbar.Brand href="/about">Venue System</Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        </Navbar>
        <Container>
          <Form
            class="d-flex justify-content-center"
            onSubmit={this.sendRequest}
          >
            <Form.Row class="d-flex justify-content-center">
              <Form.Group controlId="username">
                <Form.Label>Username</Form.Label>
                <Form.Control
                  placeholder="john-smith"
                  onChange={this.handleChange}
                />
              </Form.Group>
            </Form.Row>
            <Form.Row class="d-flex justify-content-center">
              <Form.Group controlId="password">
                <Form.Label>Password</Form.Label>
                <Form.Control
                  type="password"
                  placeholder="Password"
                  onChange={this.handleChange}
                />
              </Form.Group>
            </Form.Row>

            <Form.Row class="d-flex justify-content-center">
              <Button variant="primary" type="submit">
                Submit
              </Button>
            </Form.Row>
          </Form>
        </Container>
      </>
    );
  }
}

export default withCookies(LoginPage);
