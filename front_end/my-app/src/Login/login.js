import React from "react";
import {Navbar, Form, Button, Col, Card, Container} from "react-bootstrap";
import fetch from "fetch-with-proxy"
import { instanceOf } from 'prop-types';
import { withCookies, Cookies } from 'react-cookie';
import {Redirect} from "react-router-dom";

class LoginPage extends React.Component {
    static propTypes = {
      cookies: instanceOf(Cookies).isRequired
    };
    constructor(props) {
        super(props)
        const { cookies } = props;
        this.state = {
            request:{
                username: "",
                password: "",
            },
            resp_message: {
                message_type: "NONE",
                message: "",
            },
            show_message: false,
        }
    }

    handleChange = (event) => {
        var new_request = this.state.request;
        new_request[event.target.id] = event.target.value;
        this.setState((state) => ({request: new_request}));
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
                    console.log(result)
                  if (result.token !== null && result.token !==undefined) {
                    const { cookies } = this.props;
                    console.log("yeet")
                    cookies.set("token", result["token"], { path: '/' })
                    window.location.href="/"
                  } else {
                    
                    //this.setMessage("Successfully Logged in", "SUCCESS");
                  }
                },
                (error) => {
                  
                    //this.setMessage("ERROR sending request", "ERROR");
                }
            )
            ;
      };

    render() {
        return(
            <>
                <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
                <Navbar.Brand href="/about">Venue System</Navbar.Brand>
                <Navbar.Toggle aria-controls="responsive-navbar-nav" />
                </Navbar>
                <Container >
                    <Form class="d-flex justify-content-center" onSubmit={this.sendRequest}>
                      <Form.Row class="d-flex justify-content-center">
                          <Form.Group controlId="username" >
                              <Form.Label>Username</Form.Label>
                              <Form.Control placeholder="john-smith" onChange={this.handleChange}/>
                          </Form.Group>
                      </Form.Row>
                      <Form.Row class="d-flex justify-content-center">
                        <Form.Group controlId="password">
                          <Form.Label>Password</Form.Label>
                          <Form.Control type="password" placeholder="Password" onChange={this.handleChange}/>
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