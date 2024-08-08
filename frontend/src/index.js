import React from 'react';
import ReactDOM from 'react-dom';
import './index.css'; // Ensure this file exists in the same directory
import AppRouter from './components/AppRouter';

ReactDOM.render(
  <React.StrictMode>
    <AppRouter />
  </React.StrictMode>,
  document.getElementById('root')
);
