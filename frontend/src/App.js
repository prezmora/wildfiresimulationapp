import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import SignUp from './components/Auth/SignUp';
import Login from './components/Auth/Login';
import Verification from './components/Auth/Verification';
import MapPage from './pages/MapPage';

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/signup" component={SignUp} />
        <Route path="/login" component={Login} />
        <Route path="/verification" component={Verification} />
        <Route path="/map" component={MapPage} />
        <Route exact path="/" component={Login} />
      </Switch>
    </Router>
  );
}

export default App;
