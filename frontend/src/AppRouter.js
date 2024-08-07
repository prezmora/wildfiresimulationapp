import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Signup from './components/Auth/Signup';
import Login from './components/Auth/Login';
import MapView from './components/Map/MapView';

const AppRouter = () => (
  <Router>
    <Switch>
      <Route path="/signup" component={Signup} />
      <Route path="/login" component={Login} />
      <Route path="/map" component={MapView} />
      <Route exact path="/" component={Login} />
    </Switch>
  </Router>
);

export default AppRouter;
