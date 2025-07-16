import React from 'react';
import ReactDOM from 'react-dom/client'; // ✅ correcto
import './index.css';
import App from './App';
import * as serviceWorkerRegistration from './serviceWorkerRegistration';
import reportWebVitals from './reportWebVitals';

// 🟢 ESTE es el método moderno de montaje en React 18+
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

serviceWorkerRegistration.unregister();
reportWebVitals();