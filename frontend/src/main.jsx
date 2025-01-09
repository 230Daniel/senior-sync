import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { QueryClientProvider } from 'react-query';
import { BrowserRouter, Routes, Route } from "react-router";

import { ThemeProvider } from './layout/ThemeSelector.jsx';
import { QueryClient } from './api/api.js';

import './index.css';

import Home from './pages/Home.jsx';
import Layout from './layout/Layout.jsx';
import Metric from './pages/Metric.jsx';

// REGISTER ERROR OVERLAY
const showErrorOverlay = err => {
  // must be within function call because that's when the element is defined for sure.
  const ErrorOverlay = customElements.get('vite-error-overlay');
  // don't open outside vite environment
  if (!ErrorOverlay) { return; }
  console.log(err);
  const overlay = new ErrorOverlay(err);
  document.body.appendChild(overlay);
};

window.addEventListener('error', showErrorOverlay);
window.addEventListener('unhandledrejection', ({ reason }) => showErrorOverlay(reason));

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <QueryClientProvider client={QueryClient}>
      <ThemeProvider>
        <BrowserRouter>
          <Routes>
            <Route element={<Layout />}>
              <Route path="/" element={<Home />} />
              <Route path="/metric/:metricId" element={<Metric />} />
              <Route path="*" element={<h1 >404 Not Found</h1>} />
            </Route>
          </Routes>
        </BrowserRouter>
      </ThemeProvider>
    </QueryClientProvider>
  </StrictMode>
);
