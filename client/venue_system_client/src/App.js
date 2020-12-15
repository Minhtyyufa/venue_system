import './App.css';
import MainPage from "./Customer/main.js";
import LoginPage from "./Login/login";
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";
import React from "react";
import VenueMainPage from "./Venue/venue_owner";
import ReserveTicketPage from "./Customer/reserve_ticket";
import BuyTicketPage from "./Customer/buy_ticket";

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
            <Route path="/customer/buy_ticket">
              <BuyTicketPage/>
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

