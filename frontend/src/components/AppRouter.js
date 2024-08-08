// frontend/src/components/AppRouter.js

import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import HomePage from '../pages/HomePage';
import DashboardPage from '../pages/DashboardPage';
import MapPage from '../pages/MapPage';
import AirQualityPage from '../pages/AirQualityPage';
import LocationPage from '../pages/LocationPage';
import Login from './Auth/Login';
import Signup from './Auth/Signup';

const AppRouter = () => {
    return (
        <Router>
            <Switch>
                <Route exact path="/" component={HomePage} />
                <Route path="/dashboard" component={DashboardPage} />
                <Route path="/map" component={MapPage} />
                <Route path="/airquality" component={AirQualityPage} />
                <Route path="/location" component={LocationPage} />
                <Route path="/login" component={Login} />
                <Route path="/signup" component={Signup} />
            </Switch>
        </Router>
    );
};

export default AppRouter;
