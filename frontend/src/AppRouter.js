import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import SignUp from './components/SignUp';
import Login from './components/Login';
import Map from './components/Map';

const AppRouter = () => (
  <Router>
    <Switch>
      <Route path="/signup" component={SignUp} />
      <Route path="/login" component={Login} />
      <Route path="/map" component={Map} />
    </Switch>
  </Router>
);

export default AppRouter;
