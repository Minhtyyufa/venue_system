import logo from './logo.svg';
import './App.css';
import MainPage from "./Customer/main.js";
import LoginPage from "./Login/login";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import React from "react";
import { CookiesProvider } from 'react-cookie';
import VenueMainPage from "./Venue/venue_owner";
import ReserveTicketPage from "./Customer/reserve_ticket";

export default class App extends React.Component {

  render() {
    return (
      <Router>
        <div>
          {/* A <Switch> looks through its children <Route>s and
              renders the first one that matches the current URL. */}
          <Switch>
            <Route path="/login">
              <LoginPage />
            </Route>
            <Route path="/customer/view_tickets">
              <ReserveTicketPage/>
            </Route>
            <Route path="/venue_owner">
              <VenueMainPage/>
            </Route>
            <Route path="/">
              <MainPage/>
            </Route>
            
          </Switch>
        </div>
      </Router>
    );
  }
  
}
function Home() {
  return <h2>Home</h2>;
}

function About() {
  return <h2>About</h2>;
}

function Users() {
  return <h2>Users</h2>;
}

