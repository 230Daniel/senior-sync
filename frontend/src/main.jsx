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
