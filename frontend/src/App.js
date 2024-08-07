import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import HomePage from './pages/HomePage';
import DashboardPage from './pages/DashboardPage';
import MapPage from './pages/MapPage';
import AirQualityPage from './pages/AirQualityPage';
import LocationPage from './pages/LocationPage';
import Header from './components/Header';
import Footer from './components/Footer';
import './styles/main.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <main>
          <Switch>
            <Route exact path="/" component={HomePage} />
            <Route path="/dashboard" component={DashboardPage} />
            <Route path="/map" component={MapPage} />
            <Route path="/air-quality" component={AirQualityPage} />
            <Route path="/location" component={LocationPage} />
          </Switch>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;