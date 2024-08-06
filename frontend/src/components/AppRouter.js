import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import SignUp from './SignUp';
import Login from './Login';
import Verification from './Verification';
import AzureMap from './Map';

const AppRouter = () => (
  <Router>
    <Switch>
      <Route path="/signup" component={SignUp} />
      <Route path="/login" component={Login} />
      <Route path="/verification" component={Verification} />
      <Route path="/map" component={AzureMap} />
      <Route exact path="/" component={AzureMap} />
    </Switch>
  </Router>
);

export default AppRouter;
