import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import SignUp from './components/SignUp';
import Login from './components/Login';
import AzureMap from './components/Map';

const AppRouter = () => (
  <Router>
    <Switch>
      <Route path="/signup" component={SignUp} />
      <Route path="/login" component={Login} />
      <Route path="/map" component={AzureMap} />
      <Route exact path="/" component={Login} />
    </Switch>
  </Router>
);

export default AppRouter;
