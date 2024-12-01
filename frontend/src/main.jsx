import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import {Auth0Provider} from '@auth0/auth0-react';

const domain = 'dev-bn5zplwa13e6kgxe.us.auth0.com';
const clientId = 'l5RuNT5yNXzqVzyiBbEDWBeqv1VVnr1f';


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Auth0Provider
      domain={domain}
      clientId={clientId}
      redirectUri={window.location.origin}
    >
    <App />
    </Auth0Provider>
  </StrictMode>,
)
