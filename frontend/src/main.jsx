import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from "react-router";

import App from './App.jsx';

import './index.css';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/something" element={<h1>something</h1>} />
        <Route path="*" element={<h1 >404 Not Found</h1>} />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
);
