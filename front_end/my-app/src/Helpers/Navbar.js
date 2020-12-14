import React from "react";
import { withCookies } from "react-cookie";
import { Navbar, Nav } from "react-bootstrap";

class CustNavBar extends React.Component {
  constructor(props) {
    super(props);
  }

  destroyCookie = () => {
    const { cookies } = this.props;
    cookies.remove("token");
  };

  render() {
    return (
      <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
        <Navbar.Brand href="/">Venue System</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="ml-auto">
            <Nav.Link onClick={this.destroyCookie} href="/login">
              Logout
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    );
  }
}

export default withCookies(CustNavBar);
